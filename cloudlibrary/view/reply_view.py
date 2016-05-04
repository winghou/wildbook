# coding: utf-8
import django
import django.utils.timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from cloudlibrary.models import WildBook, WildBookReply, WildUser
from cloudlibrary.static_vars import MAX_LEN_BOOK_REPLY


@login_required
def book_reply(request):
    if request.method != "POST":
        data = {
            "res": "error",
            "title": "提示页",
            "msg": "你访问的页面不存在",
            "next_page": "/index",
        }
        return render(request, "cloudlibrary/msg.html", data)
        pass
    data_cont = {}
    try:
        book_id = request.POST.get("book_id")
        reply_text = request.POST.get("reply_text")
        if request.user.id is None:
            data_cont["res"] = "error"
            data_cont["msg"] = "请登陆后再留言"
            raise Exception()
        if reply_text is None or len(str(reply_text)) == 0:
            data_cont["res"] = "error"
            data_cont["msg"] = "请输入评论内容"
            raise Exception()
        if reply_text is None or len(str(reply_text)) > MAX_LEN_BOOK_REPLY:
            data_cont["res"] = "error"
            data_cont["msg"] = "您输入的留言内容过长,请不要多于120字"
            raise Exception()
        if book_id is None or len(str(book_id)) == 0:
            data_cont["res"] = "error"
            data_cont["msg"] = "数据接收时出现未知错误,请您保存回复内容刷新页面重试"
            raise Exception()

        try:
            # 相应图书
            reply_book = WildBook.objects.get(id=book_id)
            reply_book.newreply += 1
            # 修改最新评论时间
            reply_book.last_reply_date = django.utils.timezone.now()
            reply_book.save()
            pass
        except WildBook.DoesNotExist:
            data_cont["res"] = "error"
            data_cont["msg"] = "没有找到相应图书,可能书的主人已将其删除,请尝试刷新页面"
            raise Exception()
            pass
        # print(reply_book.name)
        book_owner = reply_book.owner
        book_owner.save()

        new_reply = WildBookReply(content=reply_text, book=reply_book, user_id=request.user.id)
        new_reply.save()
        # 添加回复通知
        pass
    except:
        if data_cont.get("msg") is None:
            data_cont["res"] = "error"
            data_cont["msg"] = "留言时出现未知错误"
        import traceback
        traceback.print_exc()
        pass
    else:
        data_cont["res"] = "success"
        pass
    return JsonResponse(data_cont)
    pass
