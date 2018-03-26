# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class District(models.Model):
    name = models.CharField(default='',max_length=50, verbose_name=u"乡镇名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"地区"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_clients_all(self):
        return self.clients_set.all()


class Clients(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"客户名称")
    district = models.ForeignKey(District,verbose_name=u"乡镇")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"客户"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
