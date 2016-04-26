# codding: utf-8
# 使用 Django 模型实现数据存储
import os
import sys

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))

# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wildteam.settings")
    django.setup()
# end

from wildteam import settings
from cloudlibrary.models import WildBook
from cloudlibrary.public.qiniu import save_file_to_qiniu


if __name__ == "__main__":
    media_path = os.path.join(settings.BASE_DIR, "media", "cloudlibrary","image")
    pic_names = os.listdir(media_path)
    for pic_name in pic_names:
        save_file_to_qiniu(img_path=os.path.join(media_path, pic_name), img_name=pic_name)
        pass
    wildbooks = WildBook.objects.all()
    for wildbook in wildbooks:
        src = wildbook.pic
        if src.find("http") < 0:
            wildbook.pic = "http://7xtddb.com2.z0.glb.clouddn.com/" + wildbook.pic
            wildbook.save()
    pass


