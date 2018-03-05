#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/29 22:43'
from django.conf.urls import url,include
from .views import UserInfoView,UploadImageView,UpdatePwdView,UpdateEmailView,MyCourseView,OrgFavView,TeacherFavView
from .views import CourseFavView,MyMessageView
urlpatterns = [#机构页面
    url(r'^user_info/$', UserInfoView.as_view(),name="user_info"),
    url(r'^upload_image/$', UploadImageView.as_view(),name="upload_image"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(),name="update_pwd"),
    url(r'^update/email/$', UpdateEmailView.as_view(),name="update_email"),
    url(r'^user_course/$', MyCourseView.as_view(),name="user_course"),
    #个人收藏机构
    url(r'^user_favorg/$', OrgFavView.as_view(),name="user_favorg"),
    #个人收藏教师
    url(r'^user_favteacher/$', TeacherFavView.as_view(),name="user_favteacher"),
    #个人收藏课程
    url(r'^user_favcourse/$', CourseFavView.as_view(),name="user_favcourse"),
    #个人消息
    url(r'^user_message/$', MyMessageView.as_view(),name="user_message"),
]