from django.urls import path
from apps.users import views

urlpatterns = [
    path('usernames/<username_valid:username>/count/', views.UserCountView.as_view()),
    path('register/', views.RegisterView.as_view()),
]