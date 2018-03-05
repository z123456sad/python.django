#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/25 23:25'
from django.conf.urls import url,include
from course.views import CourseListView,CourseDetailView,CourseVideoView,CourseCommentView,AddCommentView,UserCourseView,VideoView
urlpatterns = [#课程页面
    url(r'^list/$', CourseListView.as_view(),name="course_list"),
    #url(r'^det/$', CourseDetailView.as_view(),name="course_det"),
    url(r'^det/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name="course_det"),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(),name="course_video"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(),name="course_comment"),
    url(r'^add_comment/$', AddCommentView.as_view(),name="add_comment"),
    url(r'^info/(?P<course_id>\d+)/$', UserCourseView.as_view(), name="course_info"),
    url(r'^course_video/(?P<video_id>\d+)/$', VideoView.as_view(), name="course_video"),
]