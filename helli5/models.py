from django.db import models


class Department(models.Model):
    name = models.CharField(verbose_name='نام دپارتمان', max_length=50, blank=False)
    order =models.IntegerField(verbose_name='ترتیب', default=0, blank=False)

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    first_name = models.CharField(verbose_name='نام', max_length=30)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=30)
    img = models.ImageField(upload_to='profilePic', default="/profilePic/default.png")
    title = models.CharField(verbose_name='عنوان', max_length=50)
    description = models.CharField(verbose_name='توضیحات', max_length=200)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    active = models.BooleanField(default=True)

