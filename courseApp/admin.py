from django.contrib import admin
from helli5 import settings
import os
import shutil

from .models import *


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date')

    def delete_model(self, request, obj):
        report_id = obj.id
        obj.delete()
        reports_folder = settings.MEDIA_ROOT + '/reports/' + str(report_id)
        if os.path.isdir(reports_folder):
            shutil.rmtree(reports_folder, ignore_errors=False)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
             self.delete_model(request, obj)


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
