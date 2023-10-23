import json

from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.http import HttpResponse, JsonResponse

# Create your views here.
from apps.oauth.models import OAuthQQUser
from apps.users.models import User
from meidou_mall import settings
from utils.token_serializer import encode_token, decode_token



class QQLoginView(View):

    def get(self, request):
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state='xxx')

        login_url = oauth.get_qq_url()

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': login_url})


class QQOAuthView(View):

    def get(self, request):
        code = request.GET.get('code')

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state='xxx')

        token = oauth.get_access_token(code)
        opid = oauth.get_open_id(token)

        try:
            auth_user = OAuthQQUser.objects.get(openid=opid)
        except OAuthQQUser.DoesNotExist:
            return JsonResponse({'code': 400, 'access_token': encode_token(token)})
        else:
            user = auth_user.user
            login(request, user)

            response = JsonResponse({'code': 0, 'errmsg': 'ok'})

            response.set_cookie('username', user.username)

            return response

    def post(self, request):

        data_dict = json.loads(request.body.decode())

        mobile = data_dict.get('mobile')
        password = data_dict.get('password')
        access_token = data_dict.get('access_token')
        access_token = decode_token(access_token)

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state='xxx')

        openid = oauth.get_open_id(access_token=access_token)

        try:
            user = User.objects.get(mobile=mobile)

        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)

        else:
            if not user.check_password(password):
                JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        OAuthQQUser.objects.create(user=user, openid=openid)

        login(request, user)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        response.set_cookie('username', user.username)

        return response
