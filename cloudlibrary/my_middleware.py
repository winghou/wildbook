# coding: utf-8
from cloudlibrary.models import WildUser, WildBook


class AddUserInfoMiddleWare(object):
    """向session中添加用户信息"""
    def process_request(self, request):
        try:
            if request.user is not None and request.user.id is not None:
                user = WildUser.objects.get(id=request.user.id)
                request.session.user = user

                # 重置用户newreply
                user.newreply = 0
                books = WildBook.objects.filter(owner_id=user.id)
                for book in books:
                    user.newreply += book.newreply
                    pass
            pass
        except:
            pass
        return None
    # def process_response(self, request, response):
    #     if request.user is not None and request.user.id is not None:
    #         user = WildUser.objects.get(id=request.user.id)
    #         request.session.user = user
    #     return response
    pass
