#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/24 16:13'
from django import forms
from operation.models import UserAsk
import re


class UserAskModelForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','phone','name_course']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError(u"手机号码非法", code="phone_nvalid")
