from django.contrib import admin
from .models import Question, QuestionBlock, PosibleAnswers

# Register your models here.

class CreateAnswerinLine(admin.TabularInline):
    model = PosibleAnswers
    can_delete=False

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (CreateAnswerinLine, )
    list_display = ('id','title')
    search_fields = ('id', 'title')


class BlockAdmin(admin.ModelAdmin):
    list_display = ('block', 'frecuency', 'active')
    search_fields = ('id', 'block')
    list_filter = ('active',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionBlock, BlockAdmin)
admin.site.register(PosibleAnswers)