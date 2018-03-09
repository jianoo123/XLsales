# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from clients.models import Clients,District
from commodities.models import Commodities
# Create your models here.
class Documents(models.Model):
    client = models.ForeignKey(Clients,verbose_name=u"客户")
    district = models.ForeignKey(District,default='', verbose_name=u"乡镇")
    commodities = models.ForeignKey(Commodities,verbose_name=u"商品")
    document_id = models.CharField(max_length=10,verbose_name=u"单据号")
    sale_nums = models.IntegerField(default=0,verbose_name=u"销售数")
    money = models.IntegerField(default=0,verbose_name=u"总金额")
    remark = models.CharField(max_length=300,default='',verbose_name=u"备注")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"单据"
        verbose_name_plural = verbose_name

