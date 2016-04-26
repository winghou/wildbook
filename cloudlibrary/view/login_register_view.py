from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from cloudlibrary.models import WildUser
from cloudlibrary.view.operations import save_user_to_session


def register(request):
    return render(request, 'cloudlibrary/register.html')
    pass


def userlogin(request):
    return render(request, "cloudlibrary/login.html")
    pass


def deal_login_register(request):
    """处理POST数据
    :param request:
    """
    username = request.POST.get("email")
    password = request.POST.get("password")
    action = request.POST.get("action")

    data = {
        "res": "",
        "msg": ""
    }
    # 顶层 try
    try:
        # 处理注册请求
        if action == "register":
            # print("得到数据:", email, password, action)
            try:
                if len(username) > 25:
                    data["res"] = "error"
                    data["msg"] = "用户名过长"
                    return JsonResponse(data)
                if len(password) > 25:
                    data["res"] = "error"
                    data["msg"] = "密码过长"
                    return JsonResponse(data)
                # 新建用户
                WildUser.objects.create_user(username=username, password=password, nickname=username)
            except Exception as e:
                data["res"] = "error"
                data["msg"] = "注册时出现错误,可能你已注册"
                # print("处理注册请求时出错: ",e)
            else:
                user = authenticate(username=username, password=password)
                login(request, user)
                save_user_to_session(request, user)
                data["res"] = "success"

        # 处理登录请求
        elif action == "login":
            user = authenticate(username=username, password=password)
            # print(user)
            if user is not None:
                # print("认证成功")
                login(request, user)
                data["res"] = "success"
                # 保存用户信息到session
                save_user_to_session(request, user)
            else:
                # print("认证失败")
                data["res"] = "error"
                data["msg"] = "用户名或密码错误"
                pass
        pass
    # 顶层 except
    except Exception as e:
        data["res"] = "error"
        data["msg"] = "处理登录/注册时发生未知错误!"
        print("处理登录/注册时出错:", e)
        pass
    return JsonResponse(data)
    pass


@login_required
def wildlogout(request):
    logout(request)
    return redirect("/index")
    pass
