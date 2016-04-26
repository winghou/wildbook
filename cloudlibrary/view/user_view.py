from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from cloudlibrary.STATIC_VARS import MAX_LEN_QQ, MAX_LEN_TEL, MAX_LEN_WEIXIN, MAX_LEN_NICKNAME
from cloudlibrary.models import WildUser, WildBook
from cloudlibrary.view.operations import save_user_to_session


@login_required
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
        books = WildBook.objects.filter(owner=data_cont["viewuser"]).order_by('-id')
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
        # 设置下一页
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
            return render(request, "cloudlibrary/people_can_edit.html", data_cont)
        else:
            # print("不是本用户,返回不可以编辑的")
            return render(request, "cloudlibrary/people_can_not_edit.html", data_cont)
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

    # 从POST过来的数据中提取数据
    nickname = request.POST.get('nickname')
    if nickname is None or nickname.strip() == "":
        nickname = ""
    qq = request.POST.get('qq')
    if qq is None or qq.strip() == "":
        qq = ""
    tel = request.POST.get('tel')
    if tel is None or tel.strip() == "":
        tel = ""
    weixin = request.POST.get('weixin')
    if weixin is None or weixin.strip() == "":
        weixin = ""
    # 判断, 不可以太长
    if qq is not None and len(qq) > MAX_LEN_QQ:
        cont_data["res"] = "error"
        cont_data["msg"] = "QQ号码过长"
        return JsonResponse(cont_data)
        pass
    if tel is not None and len(tel) > MAX_LEN_TEL:
        cont_data["res"] = "error"
        cont_data["msg"] = "电话号码过长"
        return JsonResponse(cont_data)
        pass
    if weixin is not None and len(weixin) > MAX_LEN_WEIXIN:
        cont_data["res"] = "error"
        cont_data["msg"] = "微信号码过长"
        return JsonResponse(cont_data)
        pass
    if nickname is not None and len(nickname) > MAX_LEN_NICKNAME:
        cont_data["res"] = "error"
        cont_data["msg"] = "昵称过长"
        return JsonResponse(cont_data)
        pass
    try:
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
        print("更新用户信息时出错: ", e)
        pass
    else:
        # 更新session中的用户数据
        save_user_to_session(request)
        pass
    return JsonResponse(cont_data)
