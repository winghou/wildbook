# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0007_wildbook_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='wilduser',
            name='nickname',
            field=models.CharField(max_length=30, default=''),
        ),
        migrations.AlterField(
            model_name='wildbook',
            name='pic',
            field=models.CharField(max_length=50, default='default_book_pic.gif'),
        ),
    ]
