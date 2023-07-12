from django.contrib import admin
from django.urls import path, re_path, include

from . import views

app_name='questions_app'

urlpatterns = [
    path('questions/', views.ListQuestions.as_view(), name='questions_all'),
    path('respuestas/<pk>/', views.ListarRespuestas.as_view(), name='answers_all'),
    path('add_question/', views.NewQuestionView.as_view(), name='add_question'),
    path('update-question/<pk>/', views.QuestionUpdateView.as_view(), name='update_question'),
    path('blocks/', views.ListQuestionsBlock.as_view(), name='blocks_all'),
    path('add-block/', views.BlockCreateView.as_view(), name='add_block'),
    path('delete-question/<pk>/', views.delete_question, name='delete_question'),
    path('delete-block/<pk>/', views.delete_block, name='delete_block'),
    path('update-block/<pk>', views.BlockUpdateView.as_view(), name='update_block'),
]

