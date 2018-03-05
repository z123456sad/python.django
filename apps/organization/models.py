from django.db import models
from datetime import datetime

# Create your models here.


class OrgCity(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"城市名称")
    add_time = models.DateTimeField(default=datetime.now)
    city_info = models.CharField(max_length=50,verbose_name=u"城市信息")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"机构名称")
    org_info = models.TextField(verbose_name=u"机构介绍")
    category = models.CharField(default="agency",verbose_name=u'机构类别',max_length=20,choices=(("personal","个人"),("agency","教育机构"),("shool","高校")))
    image = models.ImageField(verbose_name=u"机构图片",max_length=200,upload_to="org/%y/%m")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    courses = models.IntegerField(default=0,verbose_name=u"课程数")
    address = models.CharField(verbose_name=u"机构地址",max_length=200)
    click_nums = models.IntegerField(verbose_name=u"点击数",default=0)
    city = models.ForeignKey(OrgCity,verbose_name=u"机构地址")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher(self):
        return self.get_teacher()

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name=u"教育机构")

    name = models.CharField(max_length=50,verbose_name=u"教师名字")
    job_years = models.IntegerField(verbose_name=u"工作年限",default=0)
    position = models.CharField(max_length=50,verbose_name=u"工作职位")
    company = models.CharField(max_length=50,verbose_name=u"就职公司")
    image = models.ImageField(verbose_name=u"教师头像",max_length=200,upload_to="teacher/%y/%m",default="")
    add_time = models.DateTimeField(default=datetime.now)
    feature = models.CharField(max_length=30,verbose_name=u"教学特点")
    click = models.IntegerField(verbose_name=u"点击数",default=0)

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name