# coding: utf-8
import os
import pickle

import django
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wildteam.settings")
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
django.setup()

from cloudlibrary.models import WildBook


def save_users_to_mysql():
    file = "users.data"
    print("将要写入的文件:", file)
    f = open(file, "rb")
    objs = pickle.load(f)
    for obj in objs:
        try:
            obj.save()
        except Exception as e:
            print(e)
    f.close()
    pass


def save_books_to_mysql():
    file = "books.data"
    print("将要写入的文件:", file)
    f = open(file, "rb")
    objs = pickle.load(f)
    for obj in objs:
        try:
            print(obj.name)
            new_obj = WildBook(id=obj.id, name=obj.name, description=obj.description, pic=obj.pic,
                               add_date=obj.add_date, newreply=obj.newreply, last_reply_date=obj.last_reply_date,
                               owner=obj.owner)
            new_obj.save()
        except Exception as e:
            print(e)
    f.close()
    pass


def save_historys_to_mysql():
    file = "historys.data"
    print("将要写入的文件:", file)
    f = open(file, "rb")
    objs = pickle.load(f)
    for obj in objs:
        try:
            obj.save()
        except Exception as e:
            print(e)
    f.close()
    pass


def save_replys_to_mysql():
    file = "replys.data"
    print("将要写入的文件:", file)
    f = open(file, "rb")
    objs = pickle.load(f)
    for obj in objs:
        try:
            obj.save()
        except Exception as e:
            print(e)
    f.close()
    pass


def save_all_data_to_mysql():
    save_users_to_mysql()
    save_books_to_mysql()
    save_historys_to_mysql()
    save_replys_to_mysql()
    pass


def save_all_data_to_mysql_sec():
    file_list = ["users.data", "books.data", "historys.data", "replys.data"]
    for file in file_list:
        objs = []
        try:
            with open(file, "rb") as f:
                objs = pickle.load(f)
        except Exception as e:
            print(e)
        for obj in objs:
            try:
                obj.save()
            except Exception as e:
                print(e)
        pass

if __name__ == "__main__":
    save_all_data_to_mysql_sec()
    pass

