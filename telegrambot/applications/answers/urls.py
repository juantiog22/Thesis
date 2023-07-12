from django.contrib import admin
from django.urls import path, re_path, include

from . import views

app_name='answers_app'

urlpatterns = [
    path('answers/', views.AnswersListView.as_view(), name='answers_all'),
    path('export-to-csv/', views.export_to_csv, name='export-to-csv'),

]
