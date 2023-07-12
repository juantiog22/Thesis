from django.contrib import admin
from django.urls import path, re_path, include

from . import views

app_name='usuarios_app'

urlpatterns = [
    path('', views.LoginUser.as_view(), name='user-login'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('update-user/<pk>/', views.UpdatePassword.as_view(), name='update_user'),
]

