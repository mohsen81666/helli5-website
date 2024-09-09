from django.contrib import admin
from .models import *


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(TeacherProfile)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
