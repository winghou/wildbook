# codding: utf-8
from cloudlibrary.models import WildUser
from django.contrib.auth.models import User


def save_user_to_session(request, user=None):
    """将用户信息保存到 session
    :param request: http request
    :param user: 用户
    """
    # 如果是超级管理员
    if request.user.is_superuser:
        user = User.objects.get(id=request.user.id)
        user = WildUser.get_user_from_superuser(user)
    # 如果给的参数user不是wilduser的实例, 则从request中提取用户信息
    elif not isinstance(user, WildUser):
        user = WildUser.objects.get(id=request.user.id)
    # 保存到 session
    request.session["user"] = user.format_to_dict()
    pass
