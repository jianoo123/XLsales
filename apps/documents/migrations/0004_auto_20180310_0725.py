# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-09 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20180309_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='money',
            field=models.IntegerField(default=0, verbose_name='\u603b\u91d1\u989d'),
        ),
        migrations.AddField(
            model_name='documents',
            name='remark',
            field=models.CharField(default='', max_length=300, verbose_name='\u5907\u6ce8'),
        ),
    ]