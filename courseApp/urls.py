from django.urls import path, re_path
from .views import *


urlpatterns = [
    # re_path(r'^$', courses, name='courses'),
    # path('download_zip/<int:assignment_id>/', download_zip, name='download_zip'),
    # path('add_course/', add_course, name='add_course'),
    path('add_reports/', add_reports, name='add-reports'),
    path('reports/', student_reports, name='student-reports'),
    path('reports/<int:report_id>', report_page, name='report-page'),
    # path('<int:course_id>/', course_single, name='course_single'),
    # path('<int:course_id>/download_excel', download_excel, name='download_excel'),
    # path('<int:course_id>/<int:assignment_id>/', homework, name='homework'),
]
