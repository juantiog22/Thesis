from django.contrib import admin

from .models import Context, Message

# Register your models here.

class CreateMessageinLine(admin.TabularInline):
    model = Message
    can_delete=False

class ContextAdmin(admin.ModelAdmin):
    model = Context
    inlines = (CreateMessageinLine, )
    list_display = ('id','name')
    search_fields = ('id', 'name')


admin.site.register(Context, ContextAdmin)
admin.site.register(Message)