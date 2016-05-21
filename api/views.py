# coding: utf-8
import os
import time
from urllib.parse import urljoin
from cloudlibrary.public.qiniu import save_file_to_qiniu
from api.serializers import WildUserSerializer, WildBookSerializer, WildBookReplySerializer
from cloudlibrary.db.search import search_book
from cloudlibrary.models import *
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from cloudlibrary.static_vars import *

from cloudlibrary.public.validate import validate_nickname, validate_qq, validate_tel, validate_weixin, validate_email
from wildteam import settings


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
    # print(json.loads(request.data))
    print("data:", request.data)
    print("POST:", request.POST)
    username = request.POST.get("username")
    if username is None:
        username = request.data.get("username")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")

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
    # 用户名 username
    # 密码   password
    #       bookname
    #       bookdescription
    #       bookimg
    cont_data = {}
    try:
        # 验证用户
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            cont_data["res"] = "error"
            cont_data["msg"] = "用户账号/密码错误"
            raise Exception()
        pass
        # 书名
        book_name = request.POST.get("bookname")
        if book_name is None or str(book_name).strip() == "":
            cont_data["res"] = "error"
            cont_data["msg"] = "请输入书名"
        if len(book_name) > MAX_LEN_BOOK_NAME:
            cont_data["res"] = "error"
            cont_data["msg"] = "书名过长,请少于" + str(MAX_LEN_BOOK_NAME) + "字"
            pass
        # 描述
        book_description = request.POST.get("bookdescription")
        if book_description is None:
            book_description = ""
        if len(book_description) > MAX_LEN_DESCRIPTION:
            cont_data["res"] = "error"
            cont_data["msg"] = "描述过长,请少于" + str(MAX_LEN_DESCRIPTION) + "字"
            pass
        # 图片
        img = request.FILES.get('bookimg')
        # 图片类型
        content_type = str(img.name).split('.')[-1]
        # 支持的图片类型
        support_pic_format = ["jpg", "jpeg", "png", "bmp", "gif"]
        # 图片最终的文件名
        book_img = '.'.join((str(time.time()).replace('.', ''), content_type))
        if content_type not in support_pic_format:
            cont_data["res"] = "error"
            cont_data["msg"] = "发布失败,不支持的图片格式"
            raise Exception("图片格式不正确")
            pass
        if img.size > 1024000:
            cont_data["res"] = "error"
            cont_data["msg"] = "发布失败,图片过大"
            raise Exception("图片太大")
            pass
        print(img)
        # 保存图片
        img_path = os.path.join(str(BOOK_PIC_UPLOAD_PATH), book_img)
        print(img_path)
        # print(img_path)
        with open(img_path, "wb") as f:
            for chunk in img.chunks():
                f.write(chunk)
        save_file_to_qiniu(img_path, book_img)
        book = WildBook(name=book_name, description=book_description, pic=book_img, owner_id=user.id)
        book.pic = urljoin(settings.QINIU_DOMAIN, book.pic)
        book.save()
        pass
    except:
        if cont_data.get("res") is None:
            cont_data["res"] = "error"
            cont_data["msg"] = "发布图书时发生未知错误,请重试/反馈"
        import traceback
        traceback.print_exc()
        pass
    else:
        cont_data["res"] = "success"
        cont_data["msg"] = "发布成功"
    return Response(cont_data)


@api_view(['POST'])
def del_book(request):
    """删除书籍API"""
    data = {}
    username = request.POST.get("username")
    if username is None:
        username = request.data.get("username")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")
    bookid = request.POST.get("bookid")
    if bookid is None:
        bookid = request.data.get("bookid")
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
    if username is None:
        username = request.data.get("username")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")
    nickname = request.POST.get("nickname")
    if nickname is None:
        nickname = request.data.get("nickname")
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
    if username is None:
        username = request.data.get("username")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")
    qq = request.POST.get("qq")
    if qq is None:
        qq = request.data.get("qq")
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
    if username is None:
        username = request.data.get("username")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")
    tel = request.POST.get("tel")
    if tel is None:
        tel = request.data.get("tel")
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
    if username is None:
        username = request.data.get("username")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")
    weixin = request.POST.get("weixin")
    if weixin is None:
        weixin = request.data.get("weixin")
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
    if email is None:
        email = request.data.get("email")
    password = request.POST.get("password")
    if password is None:
        password = request.data.get("password")
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


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = WildBookSerializer

    def get_queryset(self):
        books = ""
        try:
            search_content = self.request.GET.get("search_content")
            books = search_book(search_content)
            pass
        except:
            pass
        return books
        pass
    pass


class BookReplyViewSet(viewsets.ModelViewSet):
    # queryset = WildBookReply.objects.all()
    serializer_class = WildBookReplySerializer

    def get_queryset(self):
        replys = ""
        try:
            book_id = self.request.POST.get("bookid")
            if book_id is None:
                book_id = self.request.GET.get("bookid")
            print(book_id)
            replys = WildBookReply.objects.filter(book_id=book_id)
            pass
        except:
            pass
        return replys
        pass
    pass

