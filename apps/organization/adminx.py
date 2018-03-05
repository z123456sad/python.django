#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/20 1:24'
import xadmin
from xadmin import views
from .models import OrgCity,CourseOrg,Teacher
#设置主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "简历测试后台"
    site_footer = "简历测试后台"
    menu_style = "accordion"

class OrgCitylAdmin(object):
    list_display = ['name','city_info','add_time']
    search_fields = ['name','city_info']
    list_filter = ['name','city_info','add_time']

class CourseOrgAdmin(object):
    list_display = ['name','org_info','image','address','click_nums','city','add_time']
    search_fields = ['name','org_info','image','address','click_nums','city']
    list_filter = ['name','org_info','image','address','click_nums','city','add_time']


class TeacherAdmin(object):
    list_display = ['name','org','job_years','position','company','feature','add_time']
    search_fields = ['name','org','job_years','position','company','feature']
    list_filter = ['name','org','job_years','position','company','feature','add_time']




xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(OrgCity,OrgCitylAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)