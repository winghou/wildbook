# coding: utf-8
from cloudlibrary.models import WildBook, WildUser, WildBookReply
from django.contrib.auth.models import User
from rest_framework import serializers


class WildUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cloudlibrary:wilduser-detail")

    class Meta:
        model = WildUser
        fields = ('url', 'id', 'nickname', 'qq', 'tel', 'weixin', 'nickname', 'headpic', 'newreply')


class WildBookSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cloudlibrary:wildbook-detail")
    owner = WildUserSerializer()

    class Meta:
        model = WildBook
        fields = ('url', 'id', 'name', 'description', 'pic', 'add_date', 'newreply', 'owner')
    pass


class WildBookReplySerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="cloudlibrary:wildbookreply-detail")
    user = WildUserSerializer()

    class Meta:
        model = WildBookReply
        fields = ('content', 'add_date', 'user')
    pass

    # def update(self, instance, validated_data):
    #     pass
    #
    # def create(self, validated_data):
    #     pass
    #
    # id = serializers.IntegerField()
    # qq = serializers.CharField(max_length=13)
    # tel = serializers.CharField(max_length=15)
    # weixin = serializers.CharField(max_length=30)
    # nickname = serializers.CharField(max_length=30)
    # headpic = serializers.CharField(max_length=50)
    # newreply = serializers.IntegerField()

#
# class WildBookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WildBook
#         fields = ('name', 'description', 'pic', 'add_date', 'newreply', 'owner')


