#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/20 13:43'
import xadmin
from .models import Course,Chapter,Video,CourseResources

class CourseAdmin(object):
    list_display = ['name','detail','degree','student','collect','image','info','click','course_time','add_time']
    search_fields = ['name','detail','degree','student','collect','image','info','click','course_time']
    list_filter = ['name','detail','degree','student','collect','image','info','click','course_time','add_time']


class ChapterAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course','name','add_time']


class VideoAdmin(object):
    list_display = ['chapter','name','add_time']
    search_fields = ['chapter','name']
    list_filter = ['chapter','name','add_time']


class CourseResourcesAdmin(object):
    list_display = ['course','name','download','add_time']
    search_fields = ['course','name','download']
    list_filter = ['course','name','download','add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Chapter,ChapterAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResources,CourseResourcesAdmin)
