# codding: utf-8
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class WildUser(User):
    qq = models.CharField(max_length=13, default="")
    tel = models.CharField(max_length=15, default="")
    weixin = models.CharField(max_length=30, default="")
    nickname = models.CharField(max_length=30, default="")
    headpic = models.CharField(max_length=50, default="icon_default_head.jpg")

    def __str__(self):
        return "nickname:" + self.nickname + "\nqq:" + self.qq + "\n:tel" + self.tel + "\nweixin:" + self.weixin

    @staticmethod
    def get_user_from_superuser(superuser):
        return WildUser(nickname=superuser.username, username=superuser.username, email=superuser.email)
        pass

    def format_to_dict(self):
        data = {
            "username": self.username,
            "email": self.email,
            "qq": self.qq,
            "tel": self.tel,
            "weixin": self.weixin,
            "headpic": self.headpic,
            "nickname": self.nickname,
            "id": self.id,
        }
        return data
        pass
    pass


class WildBook(models.Model):
    name = models.CharField(max_length=45, default="未知")
    description = models.CharField(max_length=205, default="")
    pic = models.CharField(max_length=80, default="default_book_pic.gif")
    owner = models.ForeignKey(WildUser, default=0)

    def __str__(self):
        return self.name

    pass


class WildBookHistory(models.Model):
    """保存发布的图书的记录"""
    name = models.CharField(max_length=45, default="未知")
    description = models.CharField(max_length=200, default="")
    owner = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    pass
