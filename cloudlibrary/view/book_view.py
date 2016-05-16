# codding: utf-8
import os

import time
from urllib.parse import urljoin

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseNotModified, JsonResponse, Http404
from django.shortcuts import render

from cloudlibrary.db.common import get_oldest_unread_reply_date, get_first_level_tags
from cloudlibrary.static_vars import BOOK_PIC_UPLOAD_PATH, DEFAULT_PIC_NAME, MAX_LEN_BOOK_NAME, MAX_LEN_DESCRIPTION
from cloudlibrary.models import WildBook, WildUser, WildBookHistory, WildBookReply, BookTag
from cloudlibrary.public.qiniu import save_file_to_qiniu, del_pic_from_qiniu
from wildteam import settings
from wildteam.settings import BASE_DIR


@login_required
def add_book(request):
        # 标签
    tag_bgc_list = ['label-default', 'label-primary', 'label-success', 'label-warning',
                    'label-danger', 'label-info']

    book_tags = list(get_first_level_tags())
    book_tag_first = book_tags[0:5]
    book_tag_second = book_tags[5:]
    data_content = {
        "tag_bgc_list": tag_bgc_list,
        "book_tag_first": book_tag_first,
        "book_tag_second": book_tag_second,
    }

    return render(request, "cloudlibrary/add_book.html", data_content)
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

        # 先不从七牛删除, 空间那么多
        # # 从七牛删除相应图片
        # try:
        #     if img_path.find(DEFAULT_PIC_NAME) < 0:
        #         del_pic_from_qiniu(book.pic)
        #     pass
        # except Exception as e:
        #     print("从七牛删除图片时出错:", e)
        #     pass
        # pass
        # 执行删除

        book.delete()
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

        # print(request.POST)
        # 添加标签, 必须先添加图书再添加书签
        tag_ids = request.POST.getlist("tag_select")
        # print(tag_ids)
        if tag_ids is not None and len(tag_ids) > 0:
            for tag_id in tag_ids:
                tag = BookTag.objects.get(id=tag_id)
                # print("得到tag:", tag)
                book.tags.add(tag)
            pass

    except:
        cont_data["res"] = "error"
        if cont_data.get("msg") is None:
            cont_data["msg"] = "发布时出错"
        cont_data["next_page"] = "/addbook"

        import traceback
        traceback.print_exc()

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


def book_detail(request, book_id, page=1):
    # 直接受get请求
    data_cont = {}
    try:
        if request.method != "GET":
            raise Exception()
        book_id = int(book_id)
        view_book = WildBook.objects.get(id=book_id)
        view_user = view_book.owner

        # 如果浏览书的是书的主人,要处理
        if view_user.id == request.user.id:
            view_user.newreply -= view_book.newreply
            view_user.newreply = max(0, view_user.newreply)
            view_user.save()
            view_book.newreply = 0

            # 修改最新回复时间,让其沉底
            # print(get_oldest_unread_reply_date(view_user.id))
            view_book.last_reply_date = get_oldest_unread_reply_date(view_user.id)
            view_book.save()
            # 修改session中的 newreply信息
            request.session.user.newreply = view_user.newreply
            pass

        # 得到回复并分页
        view_book_replys = WildBookReply.objects.filter(book=view_book).order_by('-id')

        # 分页
        try:
            page = int(page)
            if page < 1:
                page = 1
            pass
        except:
            page = 1
            pass
        # 每页显示记录数量
        reply_cnt_per_page = 10
        book_page_list = Paginator(view_book_replys, reply_cnt_per_page)
        # 总分页数
        total_page = book_page_list.num_pages
        try:
            replys_cur_page = book_page_list.page(page)
            pass
        except EmptyPage:
            replys_cur_page = book_page_list.page(total_page)
            page = total_page
            pass
        except Exception:
            replys_cur_page = book_page_list.page(1)
            page = 1
            pass
        # 分页信息返回
        data_cont["page1st"] = page - 2
        data_cont["page2ed"] = page - 1
        data_cont["page3th"] = page
        data_cont["page4th"] = page + 1 if page + 1 <= total_page else -1
        data_cont["page5th"] = page + 2 if page + 2 <= total_page else -1
        data_cont["page_first"] = 1
        data_cont["page_last"] = total_page

        # 标签
        data_cont["tag_bgc_list"] = ['label-default', 'label-primary', 'label-success', 'label-warning',
                                     'label-danger', 'label-info']
        view_book.tag_list = list(view_book.tags.all())
        # 填写返回的信息
        data_cont["viewbook"] = view_book
        data_cont["viewuser"] = view_user
        data_cont["replys"] = replys_cur_page

        pass
    except:
        import traceback
        traceback.print_exc()
        data_cont = {
            "res": "error",
            "msg": "你访问的页面不存在",
            "next_page": "/index",
        }
        return render(request, "cloudlibrary/msg.html", data_cont)
        pass
    return render(request, 'cloudlibrary/bookdetail.html', data_cont)
    pass
