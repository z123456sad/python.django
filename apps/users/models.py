from django.db import models
from datetime import datetime
# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default="")
    birthday = models.DateField(verbose_name=u"生日",null=True,blank=True)
    gender = models.CharField(choices=(("male",u"男"),("female",u"女")),max_length=6,default="female")
    address = models.CharField(max_length=500,blank=True,null=True,verbose_name=u"地址")
    phone = models.CharField(max_length=11,verbose_name=u"手机号",null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%M",max_length=500,default="image/default.png")

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def user_unread_message(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user_id=self.id).count()

class EmailVerification(models.Model):
    myemail = models.EmailField(max_length=50,verbose_name=u"邮箱")
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    send_type = models.CharField(choices=(("register",u"注册验证码"),("forget",u"忘记验证码"),("update",u"修改邮箱")),max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.myemail)
class Carousel(models.Model):
    add_time = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=30,verbose_name=u"图片名字")
    image =models.ImageField(upload_to="carousel/%y/%m",max_length=200,verbose_name=u"轮播图")
    urls = models.URLField(max_length=200,verbose_name=u"图片地址")
    index = models.IntegerField(verbose_name=u"顺序控制",default=100)

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name