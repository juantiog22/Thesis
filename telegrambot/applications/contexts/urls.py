from django.contrib import admin
from django.urls import path, re_path, include

from . import views

app_name='contexts_app'

urlpatterns = [
    path('contexts/', views.ListContexts.as_view(), name='contexts_all'),
    path('add-context/', views.NewContextView.as_view(), name='add_context'),
    path('update-context/<pk>/', views.ContextUpdateView.as_view(), name='update_context'),
    path('delete-context/<pk>/', views.delete, name='delete'),
]
