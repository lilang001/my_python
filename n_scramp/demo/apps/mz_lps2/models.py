# -*- coding: utf-8 -*-

"""
@author : Jackie
@date : 2015/11/11
@note :
"""
from django.db import models


class AsyncMethod(models.Model):
    CALC_TYPES = (
        ('1','计算学力'),
        ('2','完成评测模块'),
    )
    name = models.CharField(u"名称",null = True,blank= True, max_length=10)
    methods= models.CharField(u"方法体", null=True, blank=True, max_length=300)
    calc_type= models.SmallIntegerField(u"计算类型",choices=CALC_TYPES)
    calc_datetime=models.DateTimeField(u"计算时间",null=True,blank=True)
    submit_datetime=models.DateTimeField(u"提交时间",auto_now_add=True)
    priority=models.SmallIntegerField(u"优先级",default=3) #1,2,3:1最高
    is_calc=models.BooleanField(u"已计算",default=False) #当已计蒜=False，但是计蒜时间有值，表示预期执行的时间
    error_reason = models.CharField(u"错误原因", null=True, blank=True, max_length=300)

    class Meta:
        verbose_name = u'异步方法'
        verbose_name_plural = verbose_name
        ordering = ['-priority', 'submit_datetime', 'id']
    def __unicode__(self):
        return str(self.id)