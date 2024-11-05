from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from .utils import create_zip
from loginApp.models import StudentProfile
from django_jalali.db import models as jmodels

User = get_user_model()


class Course(models.Model):
    thumbnail = models.ImageField(upload_to="courses")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_course")
    title = models.CharField(max_length=50)
    students = models.ManyToManyField(User, related_name="students_enrolled_course")
    period = models.CharField(max_length=50)
    student_count = models.IntegerField()

    class Meta:
        unique_together = (('period', 'title'),)

    def get_absolute_url(self):
        return reverse('course_single', kwargs={
            'course_id': self.id
        })

    def __str__(self):
        return self.title


class Homework(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=400)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    @property
    def get_answers(self):
        return self.answers.all()

    @property
    def get_questions(self):
        return self.questions.all()

    # def download_all(self):
    #     zip_file = create_zip(self, self.get_answers)
    #     return zip_file

    def __str__(self):
        return self.title


def generate_file_url(self, filename):
    url = '/'.join(['homeworks', str(self.homework.course.id), str(self.homework.id), filename])
    return url


class Answers(models.Model):
    homework = models.ForeignKey(Homework, related_name="answers", on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_answer")
    upDate = models.DateTimeField(auto_now_add=True)
    HW = models.FileField(upload_to=generate_file_url)

    def get_files(self):
        files_list = []
        for ans in self.objects.all():
            files_list.append(ans.HW)
        return files_list
    # def get_absolute_url(self):
    #     return reverse('', kwargs={
    #         'pk': self.pk
    #     })


class Question(models.Model):
    homework = models.ForeignKey(Homework, related_name="questions", on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=True)
    text = models.TextField(max_length=400)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ans = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Report(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False)
    grade = models.CharField(choices=[('10', 'پایه ی دهم'),
                                      ('11', 'پایه ی یازدهم'),
                                      ('12', 'پایه ی دوازدهم')],
                max_length=2, null=False, blank=False)
    field = models.CharField(choices=[('R', 'رشته ریاضی'),
                                      ('T', 'رشته تجربی'),
                                      ('E', 'رشته انسانی')],
                max_length=1, null=False, blank=False)
    date = jmodels.jDateField(null=False, blank=False)

    def __str__(self):
        return f"{self.title}({self.grade}/{self.field})"


class StudentReport(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    report_url = models.CharField(max_length=128, blank=False)
    show_to_student = models.BooleanField(default=True)

    def __str__(self):
        return self.report.title + ' - ' + str(self.student.student_id)

