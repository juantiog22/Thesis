from django.contrib import admin

from .models import Answer

from applications.questions.models import Question, PosibleAnswers

# Register your models here.

class AnswersbySuscriber(admin.ModelAdmin):
    list_display = ('question', 'response', 'suscriber', 'date')

    class Meta:
        model = Answer

admin.site.register(Answer, AnswersbySuscriber)