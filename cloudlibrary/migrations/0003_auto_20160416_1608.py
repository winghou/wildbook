# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0002_auto_20160416_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='WildBook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(default='未知', max_length=50)),
                ('description', models.CharField(default='', max_length=200)),
                ('pic', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.RenameModel(
            old_name='WildUserModel',
            new_name='WildUser',
        ),
    ]
