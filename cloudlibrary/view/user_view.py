import re
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render

from cloudlibrary.public.validate import validate_qq, validate_tel, validate_weixin, validate_user_info
from cloudlibrary.static_vars import MAX_LEN_QQ, MAX_LEN_TEL, MAX_LEN_WEIXIN, MAX_LEN_NICKNAME
from cloudlibrary.models import WildUser, WildBook
from cloudlibrary.view.operations import save_user_to_session


def person_info(request, uid=None, page=1):
    try:
        data_cont = {}
        try:
            page = int(page)
            if page < 1:
                page = 1
        except Exception:
            page = 1

        # print(uid)
        # 如果是本人
        if uid is None or uid == request.user.id:
            data_cont["viewuser"] = data_cont["user"]
        # 如果不是本人
        else:
            query_user = WildUser.objects.get(id=uid)
            data_cont["viewuser"] = query_user

        # 分页
        # 得到所有发布的图书
        books = WildBook.objects.filter(owner=data_cont["viewuser"]).order_by('-last_reply_date', '-newreply')
        book_cnt_per_page = 10
        book_page_list = Paginator(books, book_cnt_per_page)
        total_page = book_page_list.num_pages
        try:
            books_cur_page = book_page_list.page(page)
            pass
        except EmptyPage:
            books_cur_page = book_page_list.page(total_page)
            page = total_page
            pass
        except Exception:
            books_cur_page = book_page_list.page(1)
            page = 1
            pass

        for book in books_cur_page:
            # 设置标签
            book.tag_list = list(book.tags.all())
            # print(book.tag_list)
        # 标签颜色随机
        tag_bgc_list = ['label-default', 'label-primary', 'label-success', 'label-warning', 'label-danger',
                        'label-info']
        #  设置下一页
        data_cont["books"] = books_cur_page,
        data_cont["page1st"] = page - 2
        data_cont["page2ed"] = page - 1
        data_cont["page3th"] = page
        data_cont["page4th"] = page + 1 if page + 1 <= total_page else -1
        data_cont["page5th"] = page + 2 if page + 2 <= total_page else -1
        data_cont["page_first"] = 1
        data_cont["page_last"] = total_page
        # 分页 end

        data_cont["books"] = books_cur_page

        if request.user.id == data_cont["viewuser"].id:
            # print("是本用户,返回可以编辑的")
            data_cont["can_edit"] = True
        else:
            # print("不是本用户,返回不可以编辑的")
            data_cont["can_edit"] = False
            pass
        return render(request, "cloudlibrary/people.html", data_cont)
        pass
    except:
        import traceback
        traceback.print_exc()
        data_cont = {
            "msg": "你访问的页面不存在",
            "res": "error",
            "next_page": "/index"
        }
        return render(request, "cloudlibrary/msg.html", data_cont)
        pass
    pass


@login_required
def edit_person(request):
    # 处理非法请求
    if request.method != "POST":
        data = {
            "res": "error",
            "title": "提示页",
            "msg": "非法请求",
            "next_page": "/index",
        }
        return render(request, "cloudlibrary/msg.html", data)
        pass

    cont_data = {}

    try:
        # 从POST过来的数据中提取数据
        # print(request.POST)
        nickname = request.POST.get('nickname')
        if nickname is None:
            nickname = nickname.strip()
        qq = request.POST.get('qq')
        if qq is None:
            qq = qq.strip()
        tel = request.POST.get('tel')
        if tel is None:
            tel = tel.strip()
        weixin = request.POST.get('weixin')
        if weixin is None:
            weixin = weixin.strip()
        # 判断, 不可以太长
        if not validate_qq(qq):
            cont_data["res"] = "error"
            cont_data["msg"] = "请输入正确的QQ号码"
            raise Exception()
            pass
        if not validate_tel(tel):
            cont_data["res"] = "error"
            cont_data["msg"] = "请输入正确的手机号码"
            raise Exception()
            pass
        if not validate_weixin(weixin):
            cont_data["res"] = "error"
            cont_data["msg"] = "微信格式不正确,微信帐号支持6-20个字母、数字、下划线和减号，必须以字母开头"
            raise Exception()
            pass
        if nickname is not None and len(nickname) > MAX_LEN_NICKNAME:
            cont_data["res"] = "error"
            cont_data["msg"] = "昵称过长(" + str(MAX_LEN_NICKNAME) + "字内)"
            raise Exception()
            pass
        if nickname is not None and len(nickname) == 0:
            cont_data["res"] = "error"
            cont_data["msg"] = "昵称不能为空"
            raise Exception()
            pass

        # 尝试保存用户
        # 得到用户
        user = WildUser.objects.get(id=request.user.id)
        # 更新数据
        user.nickname = nickname
        user.qq = qq
        user.tel = tel
        user.weixin = weixin
        user.save()
        pass
    except Exception as e:
        pass
    else:
        # 更新session中的用户数据
        save_user_to_session(request)
        pass

    # 得到最新的用户信息
    user = WildUser.objects.get(id=request.user.id)
    cont_data["tel"] = user.tel
    cont_data["nickname"] = user.nickname
    cont_data["qq"] = user.qq
    cont_data["weixin"] = user.weixin

    return JsonResponse(cont_data)
