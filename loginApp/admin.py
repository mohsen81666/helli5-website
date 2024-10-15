from django.contrib import admin
from loginApp.models import *

# Register your models here.
admin.site.register(Subscriber)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'phone', 'role', 'force_to_change_password',)
    list_filter = ('role',)
    list_editable = ('force_to_change_password',)

    def get_name(self, obj):
            return obj.user.first_name + ' ' + obj.user.last_name
    get_name.short_description = 'Name'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'get_name', 'grade', 'field', 'educational_problem', 'financial_problem',)
    list_filter = ('grade', 'field')
    list_editable = ('grade', 'field', 'educational_problem', 'financial_problem')

    def get_name(self, obj):
            return obj.user.first_name + ' ' + obj.user.last_name
    get_name.short_description = 'Name'


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'title', 'department', 'active', 'promote')
    list_editable = ('department', 'active', 'promote')

    def get_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    get_name.short_description = 'Name'


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
