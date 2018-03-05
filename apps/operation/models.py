from django.db import models
from datetime import datetime
# Create your models here.
from users.models import UserProfile
from course.models import Course

class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name=u"咨询名字")
    phone = models.CharField(max_length=11,verbose_name=u"咨询电话")
    name_course = models.CharField(max_length=50,verbose_name=u"咨询课程名")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"咨询"
        verbose_name_plural = verbose_name

class UserMessage(models.Model):
    user_id = models.IntegerField(verbose_name=u"用户ID",default=0)
    message = models.CharField(max_length=200,verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False,verbose_name=u"消息是否已读")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"发送信息"
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u"用户")
    course = models.ForeignKey(Course,verbose_name=u"课程")
    comment = models.CharField(max_length=200,verbose_name=u"评论内容")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"课程评论"
        verbose_name_plural = verbose_name

class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u"用户")
    course = models.ForeignKey(Course,verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now)


    class Meta:
        verbose_name = u"用户学习课程"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u"用户")
    # course = models.ForeignKey(Course,verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now)
    fav_id = models.IntegerField(default=0,verbose_name=u"收藏ID控制")
    fav_type = models.IntegerField(choices=((1,"课程"),(2,"课程机构"),(3,"讲师")))

    class Meta:
        verbose_name = u"课程收藏"
        verbose_name_plural = verbose_name