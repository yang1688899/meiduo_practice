from django.urls import path
from apps.captcha import views

urlpatterns = [
    path('image_codes/<uuid>/', views.ImageCaptchaView.as_view())
]