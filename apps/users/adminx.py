#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/19 23:45'

from .models import EmailVerification,Carousel

import xadmin

class EmailVerificationAdmin(object):
    list_display = ['myemail','code','send_type','send_time']
    search_fields = ['myemail','code','send_type']
    list_filter = ['myemail','code','send_type','send_time']

class CarouselAdmin(object):

    list_display = ['title','image','urls','index','add_time']
    search_fields = ['title','image','urls','index,']
    list_filter = ['title','image','urls','index','add_time']
xadmin.site.register(EmailVerification,EmailVerificationAdmin)
xadmin.site.register(Carousel,CarouselAdmin)