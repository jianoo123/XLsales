# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-11 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodities', '0009_charge_relatecharge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='charge',
            field=models.CharField(max_length=10, verbose_name='\u5546\u54c1\u4ef7\u683c'),
        ),
    ]
