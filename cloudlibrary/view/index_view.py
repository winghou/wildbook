# codding: utf-8
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

from cloudlibrary.db.common import get_first_level_tags
from cloudlibrary.db.search import search_book
from cloudlibrary.models import WildBook


def index(request, page=1):
    try:
        if isinstance(page, str):
            page = int(page)
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

        # 得到标签
        book_tags = list(get_first_level_tags())
        book_tag_first = book_tags[0:10]
        book_tag_second = book_tags[10:]

        # 对描述字数进行限制
        max_len_desc = 80
        for book in books_cur_page:
            if len(book.description) > max_len_desc:
                book.description = book.description[0:max_len_desc]
            # 设置标签
            book.tag_list = list(book.tags.all())
            # print(book.tag_list)

        # 标签颜色随机
        tag_bgc_list = ['label-default', 'label-primary', 'label-success', 'label-warning', 'label-danger',
                        'label-info']
        data_content = {"books": books_cur_page,
                        "tag_bgc_list": tag_bgc_list,
                        "book_tag_first": book_tag_first,
                        "book_tag_second": book_tag_second,
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
    except Exception:
        import traceback
        print("主页出错:")
        traceback.print_exc()
        return render(request, "cloudlibrary/index.html")
    pass

