# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-08 23:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20180309_0757'),
        ('documents', '0002_documents_add_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documents',
            options={'verbose_name': '\u5355\u636e', 'verbose_name_plural': '\u5355\u636e'},
        ),
        migrations.AddField(
            model_name='documents',
            name='district',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='clients.District', verbose_name='\u4e61\u9547'),
        ),
    ]
