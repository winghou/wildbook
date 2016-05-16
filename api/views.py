# coding: utf-8
from api.serializers import WildUserSerializer, WildBookSerializer
from cloudlibrary.models import WildUser, WildBook
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from cloudlibrary.static_vars import MAX_LEN_NICKNAME, MAX_LEN_QQ, MAX_LEN_EMAIL, MAX_LEN_PASSWORD

from cloudlibrary.public.validate import validate_nickname, validate_qq, validate_tel, validate_weixin, validate_email


class WildUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WildUser.objects.all()
    serializer_class = WildUserSerializer


class IndexBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WildBook.objects.all().order_by("-id")
    serializer_class = WildBookSerializer
    pass


class UserBookViewSet(viewsets.ModelViewSet):
    serializer_class = WildBookSerializer

    def get_queryset(self):
        books = ""
        try:
            uid = self.request.GET.get("uid")
            books = WildBook.objects.filter(owner__id=uid)
            pass
        except:
            pass
        return books
    pass


@api_view(['POST'])
def user_login(request):
    data = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    data["username"] = username
    # data["password"] = password
    user = authenticate(username=username, password=password)
    # print(user)
    if user is not None:
        data["res"] = "success"
        data["uid"] = user.id
        pass
    else:
        data["res"] = "error"
        data["msg"] = "用户名/密码错误"
    return Response(data)
    pass


@api_view(['POST'])
def add_book(request):
    img = request.POST.get("img")
    print(img)
    pass


@api_view(['POST'])
def del_book(request):
    """删除书籍API"""
    data = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    bookid = request.POST.get("bookid")
    try:
        user = authenticate(username=username, password=password)
        # print(user)
        if user is None:
            data["res"] = "error"
            data["msg"] = "用户认证失败"
            raise Exception()
            pass

        book = WildBook.objects.get(id=bookid)

        if book.owner.id != user.id:
            data["res"] = "error"
            data["msg"] = "不是书的主人,无法删除该书籍"
            raise Exception()
        book.delete()
        pass
    except WildBook.DoesNotExist:
        data["res"] = "error"
        data["msg"] = "没有找到相应图书"
        pass
    except Exception as e:
        print(e)
        if data.get("res") is None:
            data["res"] = "error"
            data["msg"] = "删除书籍时出现未知错误"
        pass
    else:
        data["res"] = "success"
        data["msg"] = "删除成功"
        pass
    return Response(data)
    pass


@api_view(['POST'])
def edit_nickname(request):
    data = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    nickname = request.POST.get("nickname")
    try:
        user = authenticate(username=username, password=password)
        # print(user)
        if user is None:
            data["res"] = "error"
            data["msg"] = "用户认证失败"
            raise Exception()
            pass
        if nickname is None:
            data["res"] = "error"
            data["msg"] = "没有接收到新昵称"
            raise Exception()
        if validate_nickname(nickname) is False:
            data["res"] = "error"
            data["msg"] = "昵称格式不正确,不要留空或多于 " + str(MAX_LEN_NICKNAME) + " 字"
            raise Exception()
            pass
        wilduser = WildUser.objects.get(id=user.id)
        wilduser.nickname = nickname
        wilduser.save()
        pass
    except Exception as e:
        print(e)
        if data.get("res") is None:
            data["res"] = "error"
            data["msg"] = "修改昵称时出现错误"
        pass
    else:
        data["res"] = "success"
        data["msg"] = "修改成功"
        pass
    return Response(data)


@api_view(['POST'])
def edit_qq(request):
    data = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    qq = request.POST.get("qq")
    try:
        user = authenticate(username=username, password=password)
        # print(user)
        if user is None:
            data["res"] = "error"
            data["msg"] = "用户认证失败"
            raise Exception()
            pass
        if qq is None:
            data["res"] = "error"
            data["msg"] = "没有接收到新QQ"
            raise Exception()
        if validate_qq(qq) is False:
            data["res"] = "error"
            data["msg"] = "QQ格式不正确"
            raise Exception()
            pass
        wilduser = WildUser.objects.get(id=user.id)
        wilduser.qq = qq
        wilduser.save()
        pass
    except Exception as e:
        print(e)
        if data.get("res") is None:
            data["res"] = "error"
            data["msg"] = "修改QQ时出现错误"
        pass
    else:
        data["res"] = "success"
        data["msg"] = "修改成功"
        pass
    return Response(data)


@api_view(['POST'])
def edit_tel(request):
    data = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    tel = request.POST.get("tel")
    try:
        user = authenticate(username=username, password=password)
        # print(user)
        if user is None:
            data["res"] = "error"
            data["msg"] = "用户认证失败"
            raise Exception()
            pass
        if tel is None:
            data["res"] = "error"
            data["msg"] = "没有接收到新电话"
            raise Exception()
        if validate_tel(tel) is False:
            data["res"] = "error"
            data["msg"] = "电话格式不正确"
            raise Exception()
            pass
        wilduser = WildUser.objects.get(id=user.id)
        wilduser.tel = tel
        wilduser.save()
        pass
    except Exception as e:
        print(e)
        if data.get("res") is None:
            data["res"] = "error"
            data["msg"] = "修改电话时出现错误"
        pass
    else:
        data["res"] = "success"
        data["msg"] = "修改成功"
        pass
    return Response(data)


@api_view(['POST'])
def edit_weixin(request):
    data = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    weixin = request.POST.get("weixin")
    try:
        user = authenticate(username=username, password=password)
        # print(user)
        if user is None:
            data["res"] = "error"
            data["msg"] = "用户认证失败"
            raise Exception()
            pass
        if weixin is None:
            data["res"] = "error"
            data["msg"] = "没有接收到新微信"
            raise Exception()
        if validate_weixin(weixin) is False:
            data["res"] = "error"
            data["msg"] = "微信格式不正确"
            raise Exception()
            pass
        wilduser = WildUser.objects.get(id=user.id)
        wilduser.weixin = weixin
        wilduser.save()
        pass
    except Exception as e:
        print(e)
        if data.get("res") is None:
            data["res"] = "error"
            data["msg"] = "修改微信时出现错误"
        pass
    else:
        data["res"] = "success"
        data["msg"] = "修改成功"
        pass
    return Response(data)


@api_view(['POST'])
def user_register(request):
    data = {}
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        if email is None or password is None or len(str(email).strip()) == 0 or len(str(password).split()) == 0:
            data["res"] = "error"
            data["msg"] = "没有提供邮箱(email)/密码(password)"
            raise Exception()
            pass
        if len(email) > MAX_LEN_EMAIL:
            data["res"] = "error"
            data["msg"] = "邮箱长度过长,请少于" + str(MAX_LEN_EMAIL) + "字"
            raise Exception()
        if len(password) > MAX_LEN_PASSWORD:
            data["res"] = "error"
            data["msg"] = "密码过长(请少于" + str(MAX_LEN_PASSWORD) + "字)"
            raise Exception()
        if not validate_email(email):
            data["res"] = "error"
            data["msg"] = "邮箱格式不正确"
            raise Exception()
        try:
            WildUser.objects.get(username=email)
            pass
        except:
            pass
        else:
            data["res"] = "error"
            data["msg"] = "该用户名已被注册"
            return Response(data)
            pass
        # 新建用户
        WildUser.objects.create_user(username=email, password=password, nickname=email, email=email)
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        if data.get("res") is None:
            data["res"] = "error"
            data["msg"] = "注册时出现未知错误"
        pass
    else:
        data["res"] = "success"
        data["msg"] = "注册成功"
        pass
    return Response(data)
    pass
