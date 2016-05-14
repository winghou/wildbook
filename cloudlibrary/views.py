# coding: utf-8
from django.shortcuts import render
from django.http import JsonResponse
from cloudlibrary.models import Feedback


def debug(request):
    return render(request, 'cloudlibrary/bookdetail.html')
    pass


def add_feedback(request):
    """处理反馈信息"""
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
    try:
        content = request.POST.get("feedback")
        if request.user.is_authenticated():
            feedback = Feedback(content=content, user_id=request.user.id)
        else:
            feedback = Feedback(content=content)
        feedback.save()
        # print(feedback)
        pass
    except Exception as e:
        data = {
            "res": "fail",
            "msg": "保存反馈时出现错误,请稍后重试",
        }
        print("添加回馈时出错:", e)
        return JsonResponse(data)
        pass
    else:
        data = {
            "res": "success",
        }
        return JsonResponse(data)
        pass
    pass
