# codding: utf-8
from django.conf.urls import include, url
import cloudlibrary.view.index_view as index_view
import cloudlibrary.view.search_view as search_view
import cloudlibrary.view.book_view as book_view
import cloudlibrary.view.login_register_view as login_reg_view
import cloudlibrary.view.user_view as user_view

import cloudlibrary.views as views


urlpatterns = [
    # 用户登录注册
    url(r'^login/*$', login_reg_view.userlogin, name="wild_login"),
    url(r'^deal_login_register/*$', login_reg_view.deal_login_register, name="deal_login_register"),
    url('register/*$', login_reg_view.register, name="wild_register"),
    url(r'^logout/*$', login_reg_view.wildlogout, name="wild_logout"),

    # 主页
    url(r'^index/*$', index_view.index, name="index"),
    url(r'^index/page/(?P<page>\d+)/*', index_view.index, name="index_with_page"),

    # 用户信息管理
    url(r'^person/(?P<uid>[0-9]*)/*$', user_view.person_info, name="person_info"),
    url(r'^person/(?P<uid>[0-9]+)/page/(?P<page>[0-9]+)/*$', user_view.person_info, name="person_info_with_page"),
    url(r'^edit_person/*$', user_view.edit_person, name="edit_person"),

    # 书籍管理
    url(r'^addbook/*', book_view.add_book, name="addbook"),
    url(r'^deal_add_book/*', book_view.deal_add_book,name="deal_add_book"),
    url(r'^delete_book', book_view.del_book, name="del_book"),

    # 搜索
    url(r'^search/*$', search_view.index_search, name="index_search"),
    url(r'^search/page/(?P<page>\d+)/*', search_view.index_search, name="index_search_with_page"),

    # debug
    url(r'^debug/?$', views.debug),

    # 未知url跳转到主页
    url(r'^', index_view.index),
]