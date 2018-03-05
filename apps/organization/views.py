from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg,OrgCity,Teacher
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .forms import UserAskModelForm
from  operation.models import UserFavorite
from course.models import Course
import json
# Create your views here.

class OrgListView(View):
    def get(self,request):
        all_org = CourseOrg.objects.all()
        all_city = OrgCity.objects.all()
        hot_orgs = all_org.order_by("-click_nums")[:3]


        #城市ID
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        #搜索功能
        key_work = request.GET.get('keywords', "")
        if key_work:
            all_org = all_org.filter(Q(name__icontains=key_work)|Q(org_info__icontains=key_work))

        #机构类别
        category = request.GET.get('ct', "")
        if category:
            all_org = all_org.filter(category=category)

        #学习人数
        sort = request.GET.get('sort', "")
        if sort == "students":
            all_org = all_org.order_by("-students")
        elif sort == "courses":
            all_org = all_org.order_by("-courses")


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org,5, request=request)
        org_nums = all_org.count()
        orgs = p.page(page)

        return render(request,"org-list.html",{
            "all_org":orgs,
            "all_city":all_city,
            "org_nums":org_nums,
            "category":category,
            "city_id":city_id,
            "sort":sort,
            "hot_orgs":hot_orgs
        })


class AddAskUserView(View):
    def post(self,request):
        userask_from = UserAskModelForm(request.POST)
        if userask_from.is_valid():
            userask = userask_from.save(commit=True)

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}',content_type='application/json')
            #return HttpResponse(json.dumps({"status":"fail","msg":userask_from.errors}),content_type='application/json')


class OrgHomeView(View):
    def get(self,request,org_id):
        status = "home"
        org_course = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org_course.id, fav_type=2):
                has_fav = True
        all_org = org_course.course_set.all()
        all_teacher = org_course.teacher_set.all()
        return render(request,"org-detail-homepage.html",{
            "all_org":all_org,
            "all_teacher":all_teacher,
            "org_course":org_course,
            "status":status,
            "has_fav":has_fav
        })


class OrgCourseView(View):
    def get(self,request,org_id):
        status = "course"
        org_course = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=org_course.id):
                has_fav = True
        all_org = org_course.course_set.all()
        all_teacher = org_course.teacher_set.all()
        return render(request,"org-detail-course.html",{
            "all_org":all_org,
            "all_teacher":all_teacher,
            "org_course":org_course,
            "status":status,
            "has_fav":has_fav
        })

class OrgDescView(View):
    def get(self,request,org_id):
        status = "desc"
        org_course = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=org_course.id):
                has_fav = True
        all_org = org_course.course_set.all()
        all_teacher = org_course.teacher_set.all()
        return render(request,"org-detail-desc.html",{
            "all_org":all_org,
            "all_teacher":all_teacher,
            "org_course":org_course,
            "status":status,
            "has_fav":has_fav
        })

class OrgTeachersView(View):
    def get(self,request,org_id):
        status = "teachers"
        org_course = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=org_course.id):
                has_fav = True
        all_org = org_course.course_set.all()
        all_teacher = org_course.teacher_set.all()
        return render(request,"org-detail-teachers.html",{
            "all_org":all_org,
            "all_teacher":all_teacher,
            "org_course":org_course,
            "status":status,
            "has_fav":has_fav
        })

class AddFavView(View):
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
        exist_recode = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_recode:
            exist_recode.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}',content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}',content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}',content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get('sort', "")
        #搜索功能
        key_work = request.GET.get('keywords', "")
        if key_work:
            all_teacher = all_teacher.filter(Q(name__icontains=key_work))

        if sort == "hot":
            all_teacher = all_teacher.order_by("-click")
        rank_teacher = all_teacher.order_by("-click")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher,5, request=request)
        teacher = p.page(page)

        return render(request,"teachers-list.html",{
            "all_teacher":teacher,
            "rank_teacher":rank_teacher

        })

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        all_teacher = Teacher.objects.get(id=int(teacher_id))
        all_course = Course.objects.filter(teacher=all_teacher)
        rank_teacher = Teacher.objects.all().order_by("-click")
        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_id=teacher_id,fav_type=3):
            has_teacher_fav = True
        return render(request,"teacher-detail.html",{
            "all_teacher":all_teacher,
            "all_course":all_course,
            "rank_teacher":rank_teacher,
            "has_teacher_fav":has_teacher_fav
        })











