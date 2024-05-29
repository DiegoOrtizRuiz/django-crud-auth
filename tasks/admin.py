from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    
admin.site.register(Tasks, TasksAdmin)
# Register your models here.
