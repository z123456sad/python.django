from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile,EmailVerification,Carousel
from django.views.generic.base import View
from .froms import LoginFrom,RegisterFrom,ForgetPwdFrom,UploadImageFrom,UpdatePwdFrom,UpdateInfoFrom
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from course.models import Course

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user1 = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user1.check_password(password):
                return user1
        except Exception as e:
            return None

class ActiveUserView(View):
    def get(self,request,active_code):
        all_recodes = EmailVerification.objects.filter(code=active_code)
        if all_recodes:
            for recode in all_recodes:
                email = recode.myemail
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request,'login.html')
        else:
            return render(request,'register.html')



class RegisterView(View):
    def get(self,request):
        register_froms = RegisterFrom()
        return render(request,'register.html',{'register_froms':register_froms})

    def post(self,request):
        register_froms = RegisterFrom(request.POST)
        if register_froms.is_valid():
            user_name = request.POST.get("email","")
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'msg':"用户名已存在"})
            pass_word = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,"register")

        return render(request,'register.html',{'register_froms':register_froms})

class LogOutView(View):
    def get(self,request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        login_froms = LoginFrom(request.POST)
        if login_froms.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request,'register.html',{'msg':"账户未激活"})
            else:
                return render(request,'login.html',{'msg':"用户名密码错误"})
        else:
            return render(request,'login.html',{'login_froms':login_froms})



class ForgetPwdView(View):
    def get(self,request):
        forget_froms = RegisterFrom()
        return render(request,'forgetpwd.html',{'forget_froms':forget_froms})

    def post(self,request):
        forget_froms = ForgetPwdFrom(request.POST)
        if forget_froms.is_valid():
            email = request.POST.get("email","")
            user = UserProfile.objects.filter(email=email)
            if user:
                send_register_email(email,"forget")
                return render(request,'send_success.html')

        return render(request,'forgetpwd.html',{'forget_froms':forget_froms})

class ModifyPwdView(View):
    def post(self,request):
        pwd = request.POST.get("password","")
        pwd1 = request.POST.get("password1","")
        email = request.POST.get("email","")
        if pwd != pwd1:
            return render(request,'password_reset.html',{"msg":"两次密码不一致"})
        user = UserProfile.objects.get(email=email)
        user.password = make_password(pwd)
        user.save()
        return render(request,'password_reset.html')




class ResetUserView(View):
    def get(self,request,active_code):
        all_recodes = EmailVerification.objects.filter(code=active_code)
        if all_recodes:
            for recode in all_recodes:
                email = recode.myemail
                return render(request,'password_reset.html',{"email":email})
        else:
            return render(request,'forgetpwd.html',{'msg':"激活链接失效"})



class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"usercenter-info.html",{

        })

    def post(self,request):
        user_info_from = UpdateInfoFrom(request.POST,instance=request.user)
        if user_info_from.is_valid():
            user_info_from.save()
            return HttpResponse('{"status":"success", "修改成功":""}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "修改失败":""}',content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        up_from = UploadImageFrom(request.POST,request.FILES,instance=request.user)
        if up_from:
            up_from.save()
            return HttpResponse('{"status":"success", "修改成功":""}',content_type='application/json')
        return HttpResponse('{"status":"fail", "修改失败":""}',content_type='application/json')

class UpdatePwdView(LoginRequiredMixin,View):
    def post(self,request):
        up_pwd = UpdatePwdFrom(request.POST)
        if up_pwd.is_valid():
            pwd = request.POST.get("password","")
            pwd1 = request.POST.get("password1","")
            if pwd != pwd1:
                return HttpResponse('{"status":"fail", "修改失败":""}',content_type='application/json')
            user = request.user
            user.password = make_password(pwd)
            user.save()
            return HttpResponse('{"status":"success", "修改成功":""}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(up_pwd.errors),content_type='application/json')

class UpdateEmailView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get("email","")
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'status':'fail', '邮箱已存在':''}",content_type='application/json')
        send_register_email(email,"update")
        return HttpResponse("{'status':'success', '修改成功':''}",content_type='application/json')

    def post(self,request):
        code = request.POST.get("code","")
        myemail = request.POST.get("email","")
        email = EmailVerification.objects.filter(code=code,send_type="update",myemail=myemail)
        if email:
            user = request.user
            user.email = myemail
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        my_course = UserCourse.objects.filter(user=request.user)
        return render(request,"usercenter-mycourse.html",{
            "my_course":my_course
        })

class OrgFavView(LoginRequiredMixin,View):
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,"usercenter-fav-org.html",{
            "org_list":org_list
        })

class TeacherFavView(LoginRequiredMixin,View):
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_org in fav_teachers:
            teacher_id = fav_org.fav_id
            org = Teacher.objects.get(id=teacher_id)
            teacher_list.append(org)

        return render(request,"usercenter-fav-teacher.html",{
            "teacher_list":teacher_list
        })

class CourseFavView(LoginRequiredMixin,View):
    def get(self,request):
        course_list = []
        fav_course = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_org in fav_course:
            course_id = fav_org.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request,"usercenter-fav-course.html",{
            "course_list":course_list
        })



class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_message = UserMessage.objects.filter(user_id=request.user.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message,5, request=request)
        message = p.page(page)

        return render(request,"usercenter-message.html",{
            "message":message
        })

class IndexView(View):
    #首页
    def get(self,request):

        all_carousel = Carousel.objects.all().order_by('index')
        all_course = Course.objects.filter(is_adv=False)
        adv_course = Course.objects.filter(is_adv=True)
        all_org = CourseOrg.objects.all()
        return render(request,"index.html",{
            "all_carousel":all_carousel,
            "all_course":all_course,
            "adv_course":adv_course,
            "all_org":all_org

        })


def not_page_found(request):
    #404页面
    from django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code = 404
    return response

def server_error(request):
    #500页面
    from django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code = 500
    return response