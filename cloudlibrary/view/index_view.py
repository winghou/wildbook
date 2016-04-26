# codding: utf-8
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

from cloudlibrary.db.search import search_book
from cloudlibrary.models import WildBook


def index(request, page=1):
    try:
        page = int(page)
        if page < 1:
            page = 1
    except Exception as e:
        print(e)
        page = 1

    # 得到需要显示的所有图书
    books = WildBook.objects.all().order_by("-id")

    # 分页
    # 每页显示记录数量
    book_cnt_per_page = 10
    book_page_list = Paginator(books, book_cnt_per_page)
    # 总分页数
    total_page = book_page_list.num_pages
    try:
        books_cur_page = book_page_list.page(page)
        pass
    except EmptyPage:
        books_cur_page = book_page_list.page(total_page)
        page = total_page
        pass
    except Exception:
        books_cur_page = book_page_list.page(1)
        page = 1
        pass
    # 设置下一页
    data_content = {"books": books_cur_page,
                    "page1st": page - 2,
                    "page2ed": page - 1,
                    "page3th": page,
                    "page4th": page + 1 if page + 1 <= total_page else -1,
                    "page5th": page + 2 if page + 2 <= total_page else -1,
                    "page_first": 1,
                    "page_last": total_page,
                    }
    return render(request, "cloudlibrary/index.html", data_content)
    pass

