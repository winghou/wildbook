from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from cloudlibrary.models import WildUser
from cloudlibrary.public.validate import validate_email, validate_user_info
from cloudlibrary.static_vars import MAX_LEN_PASSWORD, MAX_LEN_EMAIL


def register(request):
    return render(request, 'cloudlibrary/login.html')
    pass


def userlogin(request):
    return render(request, "cloudlibrary/login.html")
    pass


def deal_login_register(request):
    """处理POST数据
    :param request:
    """
    # 对非POST请求处理
    if request.method != "POST":
        return render(request, 'cloudlibrary/msg.html', {"msg": "非法请求", "next_page": "/index", "res": "error"})
        pass

    # 得到 POST 过来的数据
    email = request.POST.get("username")
    password = request.POST.get("password")
    action = request.POST.get("action")
    # print("得到数据:", username, password, action)
    data = {}
    # 顶层 try
    try:
        # 处理注册请求
        if action == "register":
            try:
                # print(request.POST)
                # print(email, len(email), MAX_LEN_EMAIL)
                if len(email) > MAX_LEN_EMAIL:
                    data["res"] = "error"
                    data["msg"] = "邮箱长度过长,请少于" + str(MAX_LEN_EMAIL) + "字"
                    return JsonResponse(data)
                if len(password) > MAX_LEN_PASSWORD:
                    data["res"] = "error"
                    data["msg"] = "密码过长(请少于" + str(MAX_LEN_PASSWORD) + "字)"
                    return JsonResponse(data)
                if not validate_email(email):
                    data["res"] = "error"
                    data["msg"] = "邮箱格式不正确"
                    return JsonResponse(data)

                # 新建用户
                WildUser.objects.create_user(username=email, password=password, nickname=email, email=email)
            except:
                data["res"] = "error"
                data["msg"] = "注册时出现错误,可能该账号已注册,请尝试换用其他用户名注册"
                import traceback
                traceback.print_exc()
                # print("处理注册请求时出错: ",e)
            else:
                user = authenticate(username=email, password=password)
                login(request, user)
                # 已在中间件中向session添加用户信息
                # save_user_to_session(request, user)
                data["res"] = "success"

        # 处理登录请求
        elif action == "login":
            user = authenticate(username=email, password=password)
            # print(user)
            if user is not None:
                # print("认证成功")
                login(request, user)
                data["res"] = "success"

                # 保存用户信息到session
                # 已在中间件中向session添加用户信息
                # save_user_to_session(request, user)

                try:
                    wild_user = WildUser.objects.get(id=user.id)
                    # 对用户不合法的信息清空
                    validate_user_info(wild_user)
                    pass
                except:
                    print("删除用户不合法信息时出错")
                    import traceback
                    traceback.print_exc()
                    pass
            else:
                # print("认证失败")
                data["res"] = "error"
                data["msg"] = "用户名或密码错误"
                pass
        pass
    # 顶层 except
    except Exception as e:
        data["res"] = "error"
        data["msg"] = "处理登录/注册时发生未知错误"
        print("处理登录/注册时出错: ", e)
        import traceback
        traceback.print_exc()
        pass
    return JsonResponse(data)
    pass


@login_required
def wildlogout(request):
    logout(request)
    return redirect("/index")
    pass
