from django.urls import path
from apps.oauth import views

urlpatterns = [
    path('qq/authorization/', views.QQLoginView.as_view()),
    path('oauth_callback/', views.QQOAuthView.as_view()),
]