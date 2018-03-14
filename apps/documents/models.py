# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from clients.models import Clients,District
from commodities.models import FactoryToCommodity,Charge,RelateCharge
# Create your models here.
class Documents(models.Model):
    #销售部分
    client = models.ForeignKey(Clients,verbose_name=u"客户")
    district = models.ForeignKey(District,default='', verbose_name=u"乡镇")
    merchant = models.ForeignKey(FactoryToCommodity,verbose_name=u"商品")
    document_id = models.CharField(max_length=10,verbose_name=u"单据号")
    salescharge = models.ForeignKey(RelateCharge, verbose_name=u"价格")
    sale_nums = models.IntegerField(default=0,verbose_name=u"销售数")
    merchant_sums = models.IntegerField(default=0,verbose_name=u"商品总价")
    ownmoney = models.IntegerField(default=0,verbose_name=u"销售欠款")
    salessums = models.IntegerField(default=0,verbose_name=u"销售总价")
    #退货部分
    return_nums = models.IntegerField(default=0,verbose_name=u"退货数")
    returnmerchant_sums = models.IntegerField(default=0,verbose_name=u"退货商品总价")
    payback = models.IntegerField(default=0,verbose_name=u"还款")
    return_sums = models.IntegerField(default=0,verbose_name=u"销售总价")
    money = models.IntegerField(default=0,verbose_name=u"总金额")
    remark = models.CharField(max_length=300,default='',verbose_name=u"备注")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"单据"
        verbose_name_plural = verbose_name

