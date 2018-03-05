from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course,CourseResources,Video
from django.http import HttpResponse
from operation.models import UserFavorite
from organization.models import CourseOrg
from django.db.models import Q
from operation.models import CourseComment,UserCourse
# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_course = Course.objects.all()
        hot_course = Course.objects.all().order_by("-click")
        #搜索功能
        key_work = request.GET.get('keywords', "")
        if key_work:
            all_course = all_course.filter(Q(name__icontains=key_work)|Q(detail__icontains=key_work))

        #学习人数排序
        sort = request.GET.get('sort', "")
        if sort == "student":
            all_course = all_course.order_by("-student")
        elif sort == "click":
            all_course = all_course.order_by("-click")

        #课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course,3, request=request)

        course = p.page(page)
        return render(request,"course-list.html",{
            "all_course":course,
            "sort":sort,
            "hot_course":hot_course

        })

class CourseDetailView(View):
    def get(self,request,course_id):
        all_course = Course.objects.get(id=int(course_id))
        #是否收藏课程
        has_fav_course = False
        #是否收藏机构
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=all_course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=all_course.course_org.id, fav_type=2):
                has_fav_org = True
        return render(request,"course-detail.html",{
            "all_course":all_course,
            "has_fav":has_fav_course,
            "has_fav_org":has_fav_org
        })

class CourseVideoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_course = CourseResources.objects.filter(course=course)
        all_comments = CourseResources.objects.all().order_by("-id")
        return render(request, "course-video.html", {
            "course":course,
            "all_course":all_course,
            "all_comments":all_comments

        })


class CourseCommentView(View):
    def get(self,request,course_id):
        all_course = Course.objects.get(id=int(course_id))
        all_resources = CourseResources.objects.filter(course=all_course)
        all_comment = CourseComment.objects.all()
        return render(request,"course-comment.html",{
            "all_course":all_course,
            "all_resources":all_resources,
            "all_comment":all_comment
        })

class AddCommentView(View):
    # def post(self,request):
    #     if not request.user.is_authenticated():
    #         return HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
    #     course_id = request.POST.get("course_id",0)
    #     comment = request.POST.get("comments","")
    #     if course_id > 0 and comment:
    #         coures_comment = CourseComment()
    #         course = CourseComment.objects.get(id=int(course_id))
    #         coures_comment.course = course
    #         coures_comment.comment = comment
    #         coures_comment.user = request.user
    #         coures_comment.save()
    #         return HttpResponse('{"status":"success", "msg":"评论成功"}',content_type='application/json')
    #     else:
    #         return HttpResponse('{"status":"fail", "msg":"评论失败"}',content_type='application/json')
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", "")
        comments = request.POST.get("comments", "")
        if course_id  and comments:
            course_comments = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comment = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class UserCourseView(View):
    def get(self,request,course_id):
        all_course = Course.objects.get(id=int(course_id))
        all_course.student += 1
        all_course.save()
        user_courses = UserCourse.objects.filter(user=request.user, course=all_course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=all_course)
            user_course.save()
        #查询用户课程
        user_cousers = UserCourse.objects.filter(course=all_course)
        #查询用户Id
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids)[:5]
        all_resources = CourseResources.objects.filter(course=all_course)
        return render(request, "course-video.html", {
            "all_course":all_course,
            "course_resources":all_resources,
            "relate_courses":relate_courses
        })

class VideoView(View):
    def get(self,request,video_id):
        all_video = Video.objects.get(id=int(video_id))
        all_course = all_video.chapter.course
        user_courses = UserCourse.objects.filter(user=request.user, course=all_course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=all_course)
            user_course.save()
        #查询用户课程
        user_cousers = UserCourse.objects.filter(course=all_course)
        #查询用户Id
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids)[:5]
        all_resources = CourseResources.objects.filter(course=all_course)
        return render(request, "course-play.html", {
            "all_course":all_course,
            "course_resources":all_resources,
            "relate_courses":relate_courses,
            "all_video":all_video
        })

