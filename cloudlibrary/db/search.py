# codding: utf-8
from cloudlibrary.db.common import get_tag_by_name
from cloudlibrary.models import WildBook


def search_book(search_cont):
    search_cont = str(search_cont).strip()
    if search_cont is None or search_cont.strip() == "":
        books = WildBook.objects.all().order_by('-id')
        return books

    if len(search_cont) > 1 and search_cont[0] == '#':
        # 如果查看的是标签
        tag_names = search_cont.split("#")
        tag = get_tag_by_name(tag_names[1:])
        print(tag.id)
        # 得到所属标签的所有书
        books = tag.wildbook_set.all().order_by('-id')
        pass
    else:
        key_words = str(search_cont).split()
        books = WildBook.objects.filter(name__contains=search_cont.strip())
        for key in key_words:
            tset = WildBook.objects.filter(name__contains=key)
            books = books | tset
        books = books.distinct().order_by('-id')
    return books
    pass
