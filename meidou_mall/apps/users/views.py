from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.users.models import User


class UserCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':0, 'count':count, 'errmsg':'ok'})
