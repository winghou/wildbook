# codding: utf-8
from django.conf.urls import include, url
import cloudlibrary.view.index_view as index_view
import cloudlibrary.view.search_view as search_view
import cloudlibrary.view.book_view as book_view
import cloudlibrary.view.login_register_view as login_reg_view
import cloudlibrary.view.user_view as user_view
import cloudlibrary.view.reply_view as reply_view
import cloudlibrary.views as views

# restful
from rest_framework import routers
import api.views as api_views
router = routers.DefaultRouter()
router.register(r'wilduser', api_views.WildUserViewSet)
router.register(r'index_book', api_views.IndexBookViewSet)
router.register(r'user_book', api_views.UserBookViewSet, base_name='cloudlibrary')


urlpatterns = [
    # api
    url(r'^api/', include(router.urls)),
    url(r'^api/user_login/*$', api_views.user_login),
    url(r'^api/add_book/*$', api_views.add_book),
    url(r'^api/del_book/*$', api_views.del_book),
    url(r'^api/edit_nickname/*$', api_views.edit_nickname),
    url(r'^api/edit_qq/*$', api_views.edit_qq),
    url(r'^api/edit_tel/*$', api_views.edit_tel),
    url(r'^api/edit_weixin/*$', api_views.edit_weixin),
    url(r'^api/user_register/*$', api_views.user_register),

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
    url(r'^addbook/*$', book_view.add_book, name="addbook"),
    url(r'^deal_add_book/*$', book_view.deal_add_book,name="deal_add_book"),
    url(r'^delete_book/*$', book_view.del_book, name="del_book"),

    # 书籍详情
    url(r'^bookdetail/(?P<book_id>\d+)/*$', book_view.book_detail, name="book_detail_with_bookid"),
    url(r'^bookdetail/(?P<book_id>\d+)/page/(?P<page>\d+)/*$',
        book_view.book_detail, name="book_detail_with_bookid_page"),

    # 书籍回复
    # POST方法
    url(r'^book_reply/*$', reply_view.book_reply, name="book_reply"),

    # 搜索
    url(r'^search/*$', search_view.index_search, name="index_search"),
    url(r'^search/page/(?P<page>\d+)/*', search_view.index_search, name="index_search_with_page"),

    # 反馈
    url(r'^feedback/*$', views.add_feedback),

    # 关于我们
    url(r'^aboutus/*$', views.about_us, name="about_us"),

    # debug
    url(r'^debug/?$', views.debug),

    # 未知url跳转到主页
    url(r'^', index_view.index),
]