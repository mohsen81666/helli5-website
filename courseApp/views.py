from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from helli5 import settings
from helli5.decorators import has_perm
from .models import *
from .forms import *
from loginApp.models import StudentProfile
import os
import csv



# def download_zip(request, assignment_id):
#     this_assignment = Homework.objects.get(id=assignment_id)
#     files = []
#     answers = Answers.objects.all()
#     for ans in answers:
#         if assignment_id == ans.homework.id:
#             files.append(ans.HW.url)
#             print("********** ", ans.HW.url)
#     print(create_zip(this_assignment, files))

def download_excel(request, course_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
    users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for user in users:
        writer.writerow(user)
    return response


def courses(request):
    course_list = Course.objects.all()
    context = {
        'course_list': course_list
    }
    return render(request, 'courses.html', context)


def add_course(request):
    return render(request, 'add_course.html', {})


def course_single(request, course_id):
    this_course = get_object_or_404(Course, id=course_id)
    context = {
        'this_course': this_course
    }
    return render(request, 'course_single.html', context)


def homework(request, course_id, assignment_id):
    related_course = get_object_or_404(Course, id=course_id)
    this_assignment = get_object_or_404(Homework, id=assignment_id, course=related_course)
    context = {
        'this_assignment': this_assignment
    }
    return render(request, 'homework.html', context)


@has_perm('courseApp.add_report')
def add_reports(request):
    if request.method == "POST":
        form = StudentReportForm(request.POST, request.FILES)
        if form.is_valid():
            report_id = form.cleaned_data['report']
            report = Report.objects.get(id=report_id)
            files = request.FILES.getlist('files')

            folder = 'reports/' + str(report.id)
            folder_addr = settings.MEDIA_ROOT + '/' + folder
            if not os.path.isdir(folder_addr):
                os.makedirs(folder_addr)

            for file in files:
                student_id = file.name.split('.')[0]
                student_profile = StudentProfile.objects.get(student_id=student_id)
                if student_profile:
                    # Check if report already exists
                    exist_report = StudentReport.objects.filter(Q(report=report) & Q(student=student_profile))
                    if not exist_report.first():
                        # Create new report
                        student_report = StudentReport()
                        student_report.report = report
                        student_report.student = student_profile
                        student_report.report_url = settings.MEDIA_URL + folder + '/' + file.name
                        student_report.save()
                    # Save the file
                    with open(folder_addr + '/' + file.name, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)

            return redirect(add_reports)

        return HttpResponse(form.errors.items())

    context = {
        'student_report_form': StudentReportForm,
    }
    return render(request, 'add_reports.html', context)


def student_reports(request):
    user = request.user
    student_profile = StudentProfile.objects.get(user=user)
    student_reports = StudentReport.objects.filter(student=student_profile).all().order_by('-report__date')

    if student_profile.financial_problem or student_profile.educational_problem:
        context = {
            "error_message": 'برای دریافت کارنامه به مدرسه مراجعه کنید.',
        }

    else:
        reports = []
        for s_report in student_reports:
            report = {
                "id": s_report.id,
                "name": s_report.report.title,
            }
            reports.append(report)

        context = {
            'reports': reports,
        }
    return render(request, 'student_reports.html', context)


def report_page(request, report_id):
    student = StudentProfile.objects.filter(user=request.user).first()  # Get student for security purposes
    student_report = get_object_or_404(StudentReport, Q(student=student) & Q(id=report_id))
    context ={
        'student_report': student_report,
    }
    return render(request, 'report_page.html', context)
