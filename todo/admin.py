from django.contrib import admin

from .models import *

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("id", "email", "surname", "name")
    list_display_links = ("email",)

@admin.register(Token)
class Token(admin.ModelAdmin):
    pass

@admin.register(TaskGroup)
class TaskGroup(admin.ModelAdmin):
    pass

@admin.register(Task)
class Task(admin.ModelAdmin):
    pass