# coding: utf-8
import re
from cloudlibrary.static_vars import MAX_LEN_NICKNAME


def validate_qq(str_to_validate):
    try:
        if str_to_validate is None:
            return True
        str_to_validate = str(str_to_validate).strip()
        if str_to_validate == "":
            return True
        return len(re.findall("^\d{5,13}$", str_to_validate)) == 1
        pass
    except:
        return False
    pass


def validate_tel(str_to_validate):
    try:
        if str_to_validate is None:
            return True
        str_to_validate = str(str_to_validate).strip()
        if str_to_validate == "":
            return True

        if len(re.findall("^\d{4}-\d{6,8}$", str_to_validate)) == 1:
            return True
        if len(re.findall("^\+\d{10,13}$", str_to_validate)) == 1:
            return True
        if len(re.findall("^\d{6,13}$", str_to_validate)) == 1:
            return True
        return False
        pass
    except:
        return False
    pass


def validate_weixin(str_to_validate):
    try:
        if str_to_validate is None:
            return True
        str_to_validate = str(str_to_validate).strip()
        if str_to_validate == "":
            return True

        return len(re.findall(r"^[a-zA-Z][a-zA-Z0-9\-_]{5,19}$", str_to_validate)) == 1
        pass
    except:
        return False
    pass


def validate_username(str_to_validate):
    try:
        if str_to_validate is None:
            return False
        str_to_validate = str(str_to_validate).strip()
        return len(re.findall(r"^[a-zA-Z][a-zA-Z0-9_]{5,19}$", str_to_validate)) == 1
        pass
    except:
        return False
    pass


def validate_nickname(str_to_validate):
    try:
        if str_to_validate is not None and len(str_to_validate) > MAX_LEN_NICKNAME:
            return False
        if str_to_validate is not None and len(str_to_validate) == 0:
            return False
        return True
    except:
        return False


def validate_email(str_to_validate):
    try:
        if str_to_validate is None:
            return False
        str_to_validate = str(str_to_validate).strip()
        return len(re.findall(r"^([a-zA-Z0-9_\.\-])+@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$", str_to_validate)) == 1
        pass
    except:
        return False
    pass


def validate_user_info(user):
    if not validate_email(user.email):
        user.email = ""
    if not validate_qq(user.qq):
        user.qq = ""
    if not validate_tel(user.tel):
        user.tel = ""
    if not validate_weixin(user.weixin):
        user.weixin = ""
    user.save()
    return
    pass


if __name__ == "__main__":
    print(validate_weixin("ez"))
    pass
