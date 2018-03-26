# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from clients.models import Clients,District
from commodities.models import FactoryToCommodity,Charge,RelateCharge
# Create your models here.
class Documents_tr(models.Model):
    document_id = models.CharField(max_length=30, verbose_name=u"单据号")
    classify = models.CharField(choices=(("sale", u"销货"), ("return", u"退货")), default="sale", max_length=10)
    merchant = models.ForeignKey(FactoryToCommodity, verbose_name=u"商品",null=True,blank=True)
    charge = models.CharField(max_length=10, verbose_name=u"商品价格")
    sale_nums = models.CharField(max_length=10,verbose_name=u"数量")
    salessums = models.CharField(max_length=10,verbose_name=u"销售总价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


class Documents(models.Model):
    client = models.ForeignKey(Clients,verbose_name=u"客户")
    district = models.ForeignKey(District,default='', verbose_name=u"乡镇")
    document_id = models.CharField(max_length=30,verbose_name=u"单据号")
    money = models.CharField(max_length=10,verbose_name=u"总金额")
    payback = models.CharField(max_length=10,verbose_name=u"还款",null=True,blank=True)
    ownmoney = models.CharField(max_length=10,verbose_name=u"销售欠款",null=True,blank=True)
    remark = models.CharField(max_length=300,default='',verbose_name=u"备注",null=True,blank=True)
    add_time = models.DateField(default=datetime.today, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"单据"
        verbose_name_plural = verbose_name

