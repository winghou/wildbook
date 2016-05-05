# coding: utf-8
import os
import pickle
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datamigration.settings_sqlite")
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
django.setup()

from cloudlibrary.models import WildUser, WildBook, WildBookHistory, WildBookReply


def get_users_from_sqlite():
    # 查询到所有
    objs = WildUser.objects.all()
    # 保存到文件
    f = open("users.data", "wb")
    pickle.dump(objs, f)
    f.close()
    pass


def get_books_from_sqlite():
    # 查询到所有
    objs = WildBook.objects.all()
    # 保存到文件
    f = open("books.data", "wb")
    pickle.dump(objs, f)
    f.close()
    pass


def get_historys_from_sqlite():
    # 查询到所有
    objs = WildBookHistory.objects.all()
    # 保存到文件
    f = open("historys.data", "wb")
    pickle.dump(objs, f)
    f.close()
    pass


def get_replys_from_sqlite():
    # 查询到所有
    objs = WildBookReply.objects.all()
    # 保存到文件
    f = open("replys.data", "wb")
    pickle.dump(objs, f)
    f.close()
    pass


def get_all_data_from_sqlite():
    try:
        get_users_from_sqlite()
        pass
    except Exception as e:
        print(e)
        pass
    try:
        get_books_from_sqlite()
        pass
    except Exception as e:
        print(e)
        pass
    try:
        get_historys_from_sqlite()
        pass
    except Exception as e:
        print(e)
        pass
    try:
        get_replys_from_sqlite()
        pass
    except Exception as e:
        print(e)
        pass
    pass

if __name__ == "__main__":
    get_all_data_from_sqlite()
    pass
