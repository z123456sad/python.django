#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/24 18:50'
from django.conf.urls import url,include
from django.contrib import admin
from organization.views import OrgListView,AddAskUserView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeachersView,AddFavView,TeacherListView
from organization.views import TeacherDetailView
urlpatterns = [#机构页面
    url(r'^list/$', OrgListView.as_view(),name="org_list"),
    url(r'^add_ask/$', AddAskUserView.as_view(),name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(),name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(),name="org_course"),
    url(r'^de/(?P<org_id>\d+)/$', OrgDescView.as_view(),name="org_de"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeachersView.as_view(),name="org_teacher"),

    #用户收藏
    url(r'^add_fav/$', AddFavView.as_view(),name="add_fav"),

    #讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(),name="teacher_list"),
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(),name="teacher_detail"),

]
