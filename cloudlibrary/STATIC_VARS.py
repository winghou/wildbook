# codding: utf-8
import os

from wildteam import settings


# 一些静态的变量
MAX_LEN_QQ = 12
MAX_LEN_TEL = 12
MAX_LEN_WEIXIN = 20
MAX_LEN_NICKNAME = 20
MAX_LEN_BOOK_NAME = 40
BOOK_PIC_UPLOAD_PATH = os.path.join(settings.BASE_DIR, "media", "cloudlibrary", "image")
DEFAULT_PIC_NAME = "default_book_pic.gif"

