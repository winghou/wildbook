# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0004_auto_20160416_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wilduser',
            name='qq',
            field=models.CharField(max_length=12, default=None),
        ),
        migrations.AlterField(
            model_name='wilduser',
            name='tel',
            field=models.CharField(max_length=12, default=None),
        ),
        migrations.AlterField(
            model_name='wilduser',
            name='weixin',
            field=models.CharField(max_length=30, default=None),
        ),
    ]
