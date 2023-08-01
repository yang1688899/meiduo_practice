import re

from apps.users.models import User


def register_data_validate(username, password, password2, mobile, allow):

    if not all([username, password, password2, mobile, allow]):
        return {'code': 400, 'errmsg': '提交数据不全!!!'}

    if not re.fullmatch('[a-zA-z0-9_-]{5,20}', username):
        return {'code': 400, 'errmsg': '用户名格式不符合要求!!!'}

    if User.objects.filter(username=username).count():
        return {'code': 400, 'errmsg': '用户名已存在!!!'}

    if not re.fullmatch('[a-zA-z0-9_-]{5,20}', password):
        return {'code': 400, 'errmsg': '密码格式不符合要求!!!'}

    if not password == password2:
        return {'code': 400, 'errmsg': '两次密码不一致!!!'}

    if not re.fullmatch('[0-9]{11}', mobile):
        return {'code': 400, 'errmsg': '手机号格式错误!!!'}

    if User.objects.filter(mobile=mobile).count():
        return {'code': 400, 'errmsg': '手机号已被注册!!!'}

