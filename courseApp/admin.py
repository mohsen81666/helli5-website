from django.contrib import admin

from .models import *


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date')


@admin.register(StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_name', 'report', 'show_to_student')
    list_editable= ('show_to_student',)
    list_filter = ('report',)
    search_fields = ('student',)

    def get_name(self, obj):
            return obj.student.user.first_name + ' ' + obj.student.user.last_name
    get_name.short_description = 'Name'


# Register your models here.
admin.site.register(Homework)
admin.site.register(Answers)
admin.site.register(Course)
