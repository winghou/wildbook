# coding: utf-8
from api.serializers import WildUserSerializer, WildBookSerializer
from cloudlibrary.models import WildUser, WildBook
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response


class WildUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WildUser.objects.all()
    serializer_class = WildUserSerializer


class IndexBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WildBook.objects.all().order_by("-id")
    serializer_class = WildBookSerializer
    pass
    

