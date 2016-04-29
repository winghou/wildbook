# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0003_auto_20160416_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wilduser',
            name='qq',
            field=models.CharField(default=None, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='wilduser',
            name='tel',
            field=models.CharField(default=None, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='wilduser',
            name='weixin',
            field=models.CharField(default=None, max_length=30, unique=True),
        ),
    ]