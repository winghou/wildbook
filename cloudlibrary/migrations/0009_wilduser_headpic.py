# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0008_auto_20160417_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='wilduser',
            name='headpic',
            field=models.CharField(default='icon_default_head.jpg', max_length=50),
        ),
    ]
