import django_redis
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from libs.captcha.captcha import captcha


class ImageCaptchaView(View):
    def get(self, request, uuid):
        code, captcha_img_byte = captcha.generate_captcha()
        redis_cli = get_redis_connection('captcha')
        redis_cli.setex(name=uuid, time=120, value=code.lower())

        return HttpResponse(captcha_img_byte, content_type='image/jpeg')


class MessageValidView(View):
    def get(self, request, mobile):

        img_code_cli = request.GET.get('image_code').lower()
        uuid = request.GET.get('image_code_id')

        if not all([mobile, img_code_cli, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全!!!'})

        redis_cli = get_redis_connection('captcha')
        img_code_server = redis_cli.get(uuid).decode().lower()

        if not img_code_server == img_code_cli:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码错误!!!'})

        ##### pretend to send a message ######
        message_code = '123456'
        redis_cli.setex(name=mobile, value=message_code, time=300)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
