from django.contrib import admin
from loginApp.models import *

# Register your models here.
admin.site.register(Subscriber)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role', 'force_to_change_password',)
    list_filter = ('role',)
    list_editable = ('force_to_change_password',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade', 'field', 'educational_problem', 'financial_problem',)
    list_filter = ('grade', 'field')
    list_editable = ('grade', 'field', 'educational_problem', 'financial_problem')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'department', 'active', 'promote')
    list_editable = ('department', 'active', 'promote')


@admin.register(TeachingDepartment)
class TeachingDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(PreRegisteredStudent)
class PreRegistrationAdmin(admin.ModelAdmin):
    list_display = ('melli_code', 'student_first_name', 'student_last_name', 'father_first_name')
    list_filter = ('field_of_study', 'is_valid')
    search_fields = ('student_first_name', 'student_last_name', 'melli_code')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    ordering = ['seen']
    # list_display_links = ['plate']
    list_display = ('date', 'subject', 'name', 'email', 'seen')
    list_filter = ('seen', 'date')
