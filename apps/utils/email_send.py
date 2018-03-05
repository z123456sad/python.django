#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/1/21 23:30'
from users.models import EmailVerification
import random,string
from django.core.mail import send_mail
from jyxt.settings import EMAIL_FROM

def random_str():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return salt

def send_register_email(email,send_type):
    email_send = EmailVerification()
    code = random_str()
    email_send.code = code
    email_send.myemail = email
    email_send.send_type = send_type
    email_send.save()

    if send_type == "register":
        email_title = "简历测试"
        email_body = "简历测试发送内容:HTTP://192.168.1.128:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    if send_type == "forget":
        email_title = "密码找回"
        email_body = "密码找回发送内容:HTTP://192.168.1.128:8000/reset/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    if send_type == "update":
        email_title = "密码找回"
        email_body = "修改邮箱{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass