# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.
class Commodities(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"商品名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"商品"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Factory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"厂家名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"厂家"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_relate_all(self):
        return self.factorytocommodity_set.all()


class FactoryToCommodity(models.Model):
    factory = models.ForeignKey(Factory, verbose_name=u"厂家")
    commodity = models.ForeignKey(Commodities, verbose_name=u"商品")

    class Meta:
        verbose_name = u"厂家商品"
        verbose_name_plural = verbose_name

    def get_id(self):
        return self.id

    def get_merchant(self):
        merchant = self.commodity.name+' '+self.factory.name
        return merchant



class Charge(models.Model):
    charge = models.CharField(max_length=10,verbose_name=u"商品价格")

    class Meta:
        verbose_name = u"商品价格"
        verbose_name_plural = verbose_name


class RelateCharge(models.Model):
    factory = models.ForeignKey(FactoryToCommodity, verbose_name=u"厂家商品")
    charge = models.ForeignKey(Charge, verbose_name=u"价格")