#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/20 13:19'

import xadmin
from .models import UserAsk,UserMessage,UserCourse,CourseComment,UserFavorite


class UserAskAdmin(object):
    list_display = ['name','phone','name_course','add_time']
    search_fields = ['name','phone','name_course']
    list_filter = ['name','phone','name_course','add_time']


class UserMessageAdmin(object):
    list_display = ['user_id','message','has_read','add_time']
    search_fields = ['user_id','message','has_read']
    list_filter = ['user_id','message','has_read','add_time']


class CourseCommentAdmin(object):
    list_display = ['user','course','comment','add_time']
    search_fields = ['user','course','comment']
    list_filter = ['user','course','comment','add_time']


class UserCourseAdmin(object):
    list_display = ['user','course','add_time']
    search_fields = ['user','course']
    list_filter = ['user','course','add_time']

class UserFavoriteAdmin(object):
    list_display = ['user','course','fav_id','fav_type','add_time']
    search_fields = ['user','course','fav_id','fav_type']
    list_filter = ['user','course','fav_id','fav_type','add_time']



xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComment,CourseCommentAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
