# codding: utf-8
import os

from wildteam import settings


# 一些静态的变量
MAX_LEN_QQ = 13
MAX_LEN_TEL = 15
MAX_LEN_USERNAME = 25
MAX_LEN_PASSWORD = 25
MAX_LEN_WEIXIN = 20
MAX_LEN_EMAIL = 40
MAX_LEN_NICKNAME = 20
MAX_LEN_BOOK_NAME = 40
MAX_LEN_DESCRIPTION = 200
BOOK_PIC_UPLOAD_PATH = os.path.join(settings.BASE_DIR, "media", "cloudlibrary", "image")
DEFAULT_PIC_NAME = "default_book_pic.gif"

