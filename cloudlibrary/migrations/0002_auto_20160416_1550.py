# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildusermodel',
            name='qq',
            field=models.CharField(unique=True, default='', max_length=12),
        ),
        migrations.AddField(
            model_name='wildusermodel',
            name='tel',
            field=models.CharField(unique=True, default='', max_length=12),
        ),
        migrations.AddField(
            model_name='wildusermodel',
            name='weixin',
            field=models.CharField(unique=True, default='', max_length=30),
        ),
    ]
