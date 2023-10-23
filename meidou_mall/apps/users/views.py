import json
import re

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.users.models import User
from utils.user_utils import register_data_validate, UserLoginRequired
from utils.token_serializer import encode_token, decode_token


class UserCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class MobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class RegisterView(View):

    def post(self, request):
        json_str = request.body.decode()
        data_dict = json.loads(json_str)

        username = data_dict.get('username')
        password = data_dict.get('password')
        password2 = data_dict.get('password2')
        mobile = data_dict.get('mobile')
        allow = data_dict.get('allow')

        if register_data_validate(username, password, password2, mobile, allow):
            return JsonResponse(register_data_validate(username, password, password2, mobile, allow))

        user = User(username=username, password=make_password(password), mobile=mobile)
        user.save()

        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class LoginView(View):

    def post(self, request):

        json_str = request.body.decode()
        data_dict = json.loads(json_str)

        username = data_dict.get('username')
        password = data_dict.get('password')
        remembered = data_dict.get('remembered')

        # data validation

        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误!!!'})

        if re.fullmatch('1[345789]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误!!!'})

        login(request, user)

        if remembered:
            request.session.set_expiry(None)

        else:
            request.session.set_expiry(0)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', username)

        return response


class LogoutView(View):

    def delete(self, request):
        # 删除session信息
        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        response.delete_cookie('username')

        return response


class InfoView(UserLoginRequired, View):

    def get(self, request):
        user = request.user

        if user:
            info_data = {
                'username': user.username,
                'mobile': user.mobile,
                'email': user.email,
                'email_active': user.email_active
            }

            return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})

        else:
            return JsonResponse({'code': 400, 'errmsg': '请进行登录'})


from django.core.mail import send_mail
class EmailView(UserLoginRequired, View):

    def put(self, request):
        data = json.loads(request.body)

        email = data.get('email')

        if not re.fullmatch('[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
            return JsonResponse({'code': 400, 'errmsg': '邮箱格式错误'})

        user = request.user
        user.email = email

        verify_url = "http://www.meiduo.site:8080?token=%s"%encode_token(user.id)

        EMAIL_FROM = '美多商城<qi_rui_hua@163.com>'
        subjest = '邮箱验证'
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        send_mail(from_email=EMAIL_FROM,message='', html_message=html_message, subject=subjest,recipient_list=[email])


        user.save()

        return JsonResponse({'code': 0, 'errmsg': 'ok'})

