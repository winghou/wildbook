# coding: utf-8
from api.serializers import WildUserSerializer, WildBookSerializer
from cloudlibrary.models import WildUser, WildBook
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate


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
        data["result"] = "true"
        data["uid"] = user.id
        pass
    else:
        data["result"] = "false"
    return Response(data)
    pass


@api_view(['POST'])
def add_book(request):
    img = request.POST.get("img")
    print(img)
    pass