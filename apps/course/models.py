from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher


# Create your models here.

class Course(models.Model):
    name = models.CharField(verbose_name=u"课程名称",max_length=60)
    detail = models.TextField(verbose_name=u"课程介绍")
    teacher = models.ForeignKey(Teacher,verbose_name=u"教师",blank=True,null=True)
    degree = models.CharField(choices=(("primary","初级"),("mid","中级"),("highlevel","高级")),verbose_name=u"难度等级",max_length=20)
    student = models.IntegerField(verbose_name=u"学习人数",default=0)
    is_adv = models.BooleanField(default=False,verbose_name=u"是否是广告位")
    collect = models.IntegerField(verbose_name=u"收藏人数",default=0)
    image = models.ImageField(verbose_name=u"图片地址",max_length=100,upload_to="course/%y/%m")
    info = models.TextField(verbose_name=u"课程详情")
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)
    click = models.IntegerField(verbose_name=u"点击数量",default=0)
    course_time = models.IntegerField(verbose_name=u"课程时长",default=0)
    course_org = models.ForeignKey(CourseOrg,verbose_name=u"课程机构关联",null=True,blank=True)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def chap_nums(self):
        return Chapter.objects.all().count()

    def get_course_chapter(self):
        return self.chapter_set.all()



class Chapter(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名字")
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_course_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name



class Video(models.Model):
    chapter = models.ForeignKey(Chapter,verbose_name=u"章节")

    name = models.CharField(max_length=100,verbose_name=u"视频名字")
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResources(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"资源名字")
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)
    download = models.FileField(upload_to="course/resources/%y/%m",max_length=100,verbose_name=u"视频资源")

    class Meta:
        verbose_name = "视频下载"
        verbose_name_plural = verbose_name