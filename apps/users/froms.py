#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/21 14:48'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class RegisterFrom(forms.Form):
    password = forms.CharField(min_length=6,required=True)
    captcha = CaptchaField()
    email = forms.EmailField(required=True)


class LoginFrom(forms.Form):
    username = forms.CharField(min_length=5,required=True)
    password = forms.CharField(min_length=6,required=True)


class ForgetPwdFrom(forms.Form):
    captcha = CaptchaField()
    email = forms.EmailField(required=True)

class UploadImageFrom(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UpdatePwdFrom(forms.Form):
    password = forms.CharField(min_length=6,required=True)

class UpdateInfoFrom(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address']