# codding: utf-8
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render, redirect
from cloudlibrary.db.search import search_book


def index_search(request, page=1):
    try:
        search_input = request.POST.get('search_input')
        if search_input is None or search_input.strip() == "":
            if page != 1:
                search_input = request.session.get('search_input')
        if search_input is None or search_input.strip() == "":
            search_input = ""

        # 如果有合法的搜索内容,保存到session
        request.session['search_input'] = search_input
        # 如果什么也没输入, 跳转到主页
        if search_input == "":
            return redirect("/index")
        try:
            page = int(page)
            if page < 1:
                page = 1
        except Exception:
            page = 1

        # 得到搜索的图书
        books = search_book(search_input)

        # 分页
        book_cnt_per_page = 10
        book_page_list = Paginator(books, book_cnt_per_page)
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
        # 设置下一页
        data_cont = {"books": books_cur_page,
                     "tag_bgc_list": tag_bgc_list,
                     "page1st": page - 2,
                     "page2ed": page - 1,
                     "page3th": page,
                     "page4th": page + 1 if page + 1 <= total_page else -1,
                     "page5th": page + 2 if page + 2 <= total_page else -1,
                     "page_first": 1,
                     "page_last": total_page}

        return render(request, "cloudlibrary/search.html", data_cont)
        pass
    except Exception as e:
        data_cont = {
            "res": "error",
            "msg": "搜索时出现错误",
            "next_page": "/index"
        }
        print(e)
        return render(request, "cloudlibrary/msg.html", data_cont)
        pass
