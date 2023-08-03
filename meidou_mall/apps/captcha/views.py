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

        redis_cli = get_redis_connection('captcha')

        send_flag = redis_cli.get('send_flag_%s'%mobile)
        if send_flag:
            return JsonResponse({'code':400, 'errmsg':'验证请求过于频繁!!!'})

        if not all([mobile, img_code_cli, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全!!!'})

        img_code_server = redis_cli.get(uuid)
        if not img_code_server:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码已过期!!!'})

        if not img_code_server.decode().lower() == img_code_cli:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码错误!!!'})

        ##### pretend to send a message ######
        message_code = '123456'
        pipeline = redis_cli.pipeline()
        pipeline.setex(name=mobile, value=message_code, time=300)
        pipeline.setex(name='send_flag_%s'%mobile, value=1, time=120)
        pipeline.execute()

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
