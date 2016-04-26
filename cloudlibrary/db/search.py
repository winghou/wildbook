# codding: utf-8
from cloudlibrary.models import WildBook


def search_book(search_cont):
    if search_cont is None or search_cont.strip() == "":
        books = WildBook.objects.all()
        return books
    key_words = str(search_cont).split()
    books = WildBook.objects.filter(name__contains=search_cont.strip())
    for key in key_words:
        tset = WildBook.objects.filter(name__contains=key)
        books = books | tset
    books = books.distinct().order_by('-id')
    return books
    pass
