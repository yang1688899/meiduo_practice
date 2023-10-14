from django.urls import path
from apps.users import views

urlpatterns = [
    path('usernames/<username_valid:username>/count/', views.UserCountView.as_view()),
    path('mobiles/<mobile>/count/', views.MobileCountView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('info/', views.InfoView.as_view()),
]