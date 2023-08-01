import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.users.models import User
from utils.user_utils import register_data_validate


class UserCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
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

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
