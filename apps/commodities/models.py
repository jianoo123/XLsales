# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.
class Commodities(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"商品名称")
    charge = models.IntegerField(verbose_name=u"商品价格")
    factory = models.CharField(max_length=50,verbose_name=u"厂家名称",null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"商品"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name