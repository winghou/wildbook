# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlibrary', '0009_wilduser_headpic'),
    ]

    operations = [
        migrations.CreateModel(
            name='WildBookAdd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='未知', max_length=50)),
                ('description', models.CharField(default='', max_length=200)),
                ('pic', models.CharField(default='default_book_pic.gif', max_length=50)),
                ('owner', models.IntegerField(max_length=10, null=True)),
            ],
        ),
    ]
