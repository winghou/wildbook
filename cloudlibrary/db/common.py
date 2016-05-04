# coding: utf-8
import django.utils.timezone
# 使用 Django 模型实现数据存储
import os
import sys
# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django
    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wildteam.settings")
    django.setup()

from cloudlibrary.models import WildBook


def get_oldest_unread_reply_date(user_id):
    """给一个book_id,返回最早的未读通知时间"""
    oldest_date = django.utils.timezone.now()
    books = WildBook.objects.filter(owner_id=user_id)
    for book in books:
        if book.newreply != 0:
            oldest_date = min(oldest_date, book.last_reply_date)
            # print(book.name)
            # print(book.last_reply_date)
        pass
    # print(oldest_date)
    return oldest_date
    pass

if __name__ == "__main__":
    get_oldest_unread_reply_date(3)
    pass

