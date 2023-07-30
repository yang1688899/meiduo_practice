from django.urls import path
from apps.users import views

urlpatterns = [
    path('usernames/<username>/count', views.UserCountView.as_view()),
]