from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection


from libs.captcha.captcha import captcha


class ImageCaptchaView(View):
    def get(self, request, uuid):

        code, captcha_img_byte = captcha.generate_captcha()
        redis_cli = get_redis_connection('captcha')
        redis_cli.setex(name=uuid, time=120, value=code)

        return HttpResponse(captcha_img_byte, content_type='image/jpeg')


