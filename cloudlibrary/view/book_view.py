# codding: utf-8
import os

import time
from urllib.parse import urljoin

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotModified, JsonResponse, Http404
from django.shortcuts import render

from cloudlibrary.static_vars import BOOK_PIC_UPLOAD_PATH, DEFAULT_PIC_NAME, MAX_LEN_BOOK_NAME, MAX_LEN_DESCRIPTION
from cloudlibrary.models import WildBook, WildUser, WildBookHistory
from cloudlibrary.public.qiniu import save_file_to_qiniu, del_pic_from_qiniu
from wildteam import settings
from wildteam.settings import BASE_DIR


@login_required
def add_book(request):
    return render(request, "cloudlibrary/add_book.html")
    pass


@login_required
def del_book(request):
    # 如果不是POST方法
    if request.method != "POST":
        data = {
            "res": "error",
            "msg": "你访问的页面不存在",
            "next_page": "/index",
        }
        return render(request, "cloudlibrary/msg.html", data)
        pass
    cont_data = {}
    try:
        book_id = request.POST.get("id")
        # 如果book_id没有或者不是整数
        if book_id is None or not str(book_id).isdigit():
            cont_data["msg"] = "非法请求"
            raise Exception("非法请求")
        # 找到书
        book = WildBook.objects.get(id=book_id)
        if book is None:
            cont_data["msg"] = "没有找到书籍"
            raise Exception("没有找到书籍")
        # 如果用户不是书籍作者, 禁止删除
        if book.owner.id != request.user.id:
            cont_data["msg"] = "不允许删除其他用户书籍"
            raise Exception("不允许删除其他用户书籍")

        img_path = os.path.join(str(BOOK_PIC_UPLOAD_PATH), book.pic)
        if img_path.find(DEFAULT_PIC_NAME) < 0 and os.path.exists(img_path) and os.path.isfile(img_path):
            os.remove(img_path)
            pass
        book.delete()
        # 从七牛删除相应图片
        try:
            if img_path.find(DEFAULT_PIC_NAME) < 0:
                del_pic_from_qiniu(book.pic)
            pass
        except Exception as e:
            print("从七牛删除图片时出错:", e)
            pass
        pass
    except Exception as e:
        print(e)
        cont_data["res"] = "error"
        if cont_data.get("msg") is None:
            cont_data["msg"] = "删除时出错"
        return JsonResponse(cont_data)
        pass
    else:
        cont_data["res"] = "success"
        cont_data["msg"] = "删除成功"
        return JsonResponse(cont_data)
    pass


@login_required
def deal_add_book(request):
    # 如果不是POST方法
    if request.method != "POST":
        data = {
            "res": "error",
            "msg": "你访问的页面不存在",
            "next_page": "/index",
        }
        return render(request, "cloudlibrary/msg.html", data)
        pass
    cont_data = {}
    # 判断是否要处理添加请求
    # 如果没有联系方式, 不能添加
    cur_user = WildUser.objects.get(id=request.user.id)
    if cur_user.qq.strip() == "" and cur_user.weixin.strip() == "" and cur_user.tel.strip() == "":
        cont_data["res"] = "error"
        cont_data["msg"] = "请至少添加一种联系方式, 以方便别人联系"
        cont_data["next_page"] = "/person"
        return render(request, "cloudlibrary/msg.html", cont_data)
        pass
    # 如果没有书名, 不能添加
    book_name = str(request.POST.get("bookname"))
    if book_name is None or book_name.strip() == "":
        cont_data["res"] = "error"
        cont_data["msg"] = "请至少输入书名"
        cont_data["next_page"] = "/addbook"
        return render(request, "cloudlibrary/msg.html", cont_data)
        pass

    try:
        book = WildBook()
        book.name = book_name
        book.description = request.POST.get("bookdescription")
        imgs = request.FILES.getlist('bookimg')
        book.owner = WildUser.objects.get(id=request.user.id)
        # print(book.name, "len:", len(book.name))
        if len(book.name) > MAX_LEN_BOOK_NAME:
            cont_data["msg"] = "发布失败,题目过长"
            raise Exception("题目太长(" + str(MAX_LEN_BOOK_NAME) + "字内")
            pass
        if len(book.description) > MAX_LEN_DESCRIPTION:
            cont_data["msg"] = "发布失败,描述过长"
            raise Exception("描述过长(" + str(MAX_LEN_DESCRIPTION) + "字内")
            pass
        for img in imgs:
            content_type = str(img.name).split('.')[-1]
            support_pic_format = ["jpg", "jpeg", "png", "bmp", "gif"]
            book.pic = '.'.join((str(time.time()).replace('.', ''), content_type))
            if content_type not in support_pic_format:
                cont_data["msg"] = "发布失败,不支持的图片格式"
                raise Exception("图片格式不正确")
                pass
            if img.size > 1024000:
                cont_data["msg"] = "发布失败,图片过大"
                raise Exception("图片太大")
                pass
            # 保存图片
            img_path = os.path.join(str(BOOK_PIC_UPLOAD_PATH), book.pic)
            # print(img_path)
            with open(img_path, "wb") as f:
                for chunk in img.chunks():
                    f.write(chunk)
            save_file_to_qiniu(img_path, book.pic)
            break
        book.pic = urljoin(settings.QINIU_DOMAIN, book.pic)
        book.save()
    except:
        cont_data["res"] = "error"
        if cont_data.get("msg") is None:
            cont_data["msg"] = "发布时出错"
        cont_data["next_page"] = "/addbook"
        # print("添加书籍时出错: ", e)
        return render(request, "cloudlibrary/msg.html", cont_data)
    else:
        # 保存已发布的图书, 删除图书的时候不删除该记录
        try:
            book_history = WildBookHistory(name=book.name, description=book.description, owner=book.owner.id)
            book_history.save()
            pass
        except Exception as e:
            print("保存书籍记录时出错:", e)
            pass
        cont_data["res"] = "success"
        cont_data["msg"] = "您的图书发布成功!"
        cont_data["next_page"] = "/index"
        return render(request, "cloudlibrary/msg.html", cont_data)
    pass
