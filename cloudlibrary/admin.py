# codding: utf-8
from django.contrib import admin
from cloudlibrary.models import WildUser, WildBook, WildBookHistory

# Register your models here.


admin.site.register(WildUser)
admin.site.register(WildBook)
admin.site.register(WildBookHistory)