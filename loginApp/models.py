from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class PreRegisteredStudent(models.Model):

    #     مشخصات دانش آموز
    student_first_name = models.CharField(verbose_name='نام', max_length=30, blank=False)
    student_last_name = models.CharField(verbose_name='نام خانوادگی', max_length=40, blank=False)
    father_first_name = models.CharField(verbose_name='نام پدر', max_length=30, blank=False)
    birth_day = models.CharField(verbose_name='روز تولد', max_length=2, blank=False,
                                choices=[(str(i), str(i)) for i in range(1, 32)],
                                default='1',
                                )
    birth_month = models.CharField(verbose_name='ماه تولد', max_length=2, blank=False,
                                    choices=[
                                        ('1', 'فروردین'),
                                        ('2', 'اردیبهشت'),
                                        ('3', 'خرداد'),
                                        ('4', 'تیر'),
                                        ('5', 'مرداد'),
                                        ('6', 'شهریور'),
                                        ('7', 'مهر'),
                                        ('8', 'آبان'),
                                        ('9', 'آذر'),
                                        ('10', 'دی'),
                                        ('11', 'بهمن'),
                                        ('12', 'اسفند'),
                                    ],
                                    default='1',
                                )
    birth_year = models.CharField(verbose_name='سال تولد', max_length=4, blank=False,
                                    choices=[(str(i), str(i)) for i in range(1380, 1392)],
                                    default=1380,
                                )
    student_picture = models.ImageField(verbose_name='عکس پرسنلی دانش‌آموز', blank=True, null=True,
                                        upload_to='registerPic/',
                                        help_text='حجم عکس شما نباید بیشتر از ۵۰۰کیلوبایت باشد',
                                        )
    melli_code = models.CharField(verbose_name='کد ملی/شماره شناسنامه', max_length=10, blank=False)
    ss_id = models.CharField(verbose_name='سریال ۶رقمی شناسنامه', max_length=6, blank=False)
    ss_numerical = models.CharField(verbose_name='سری عددی ش.', max_length=2, blank=True)
    ss_alphabetical = models.CharField(verbose_name='سری حروفی ش.', max_length=3, blank=True)
    export_place = models.CharField(verbose_name='محل صدور شناسنامه', max_length=30, blank=False)
    
    birth_place_state = models.CharField(verbose_name='استان محل تولد', max_length=30, blank=False)
    birth_place_town = models.CharField(verbose_name='شهرستان محل تولد', max_length=30, blank=False)
    religion = models.CharField(verbose_name='دین', max_length=30, blank=False,
                                choices=[
                                    ('اسلام - شیعه', 'اسلام - شیعه'),
                                    ('اسلام - اهل سنت', 'اسلام - اهل سنت'),
                                    ('مسیحی', 'مسیحی'),
                                    ('کلیمی', 'کلیمی'),
                                    ('زرتشتی', 'زرتشتی'),
                                    ('آشوری', 'آشوری'),
                                ],
                                default='اسلام - شیعه',
                                )
    nationality = models.CharField(verbose_name='ملیت', max_length=30, blank=False,
                                    choices=[
                                        ('ایرانی', 'ایرانی'),
                                        ('غیرایرانی', 'غیرایرانی'),
                                    ],
                                    default='ایرانی',
                                )
    student_mail = models.EmailField(verbose_name='ایمیل دانش‌آموز', max_length=40, blank=True, null=True)
    student_phone = models.CharField(verbose_name='شماره موبایل دانش‌آموز', max_length=11, blank=False,
                                        help_text="مثال: ۰۹۱۲۳۴۵۶۷۸۹",
                                    )
    grade_at_9th = models.FloatField(verbose_name='معدل کل پایه نهم', blank=False)
    last_year_school_name = models.CharField(verbose_name='نام مدرسه‌ی قبلی', max_length=30, blank=False)
    field_of_study = models.CharField(verbose_name='رشته‌ی تحصیلی مورد علاقه', max_length=20, blank=False,
                                        choices=[
                                            ('ریاضی', 'ریاضی'),
                                            ('تجربی', 'تجربی'),
                                            ('انسانی', 'انسانی'),
                                        ],
                                    )
    field_of_olympiad = models.CharField(verbose_name='زمینه‌ی مورد علاقه در المپیاد های علمی',
                                            max_length=30, blank=True,
                                            choices=[
                                                ('ریاضی', 'ریاضی'),
                                                ('فیزیک', 'فیزیک'),
                                                ('شیمی', 'شیمی'),
                                                ('نجوم', 'نجوم'),
                                                ('کامپیوتر', 'کامپیوتر'),
                                                ('زیست', 'زیست'),
                                                ('المپیادهای حوزه انسانی', 'المپیادهای حوزه انسانی'),
                                                ('هیچکدام', 'هیچکدام'),
                                            ],
                                        )
    field_of_pajohesh = models.CharField(verbose_name='زمینه ی مورد علاقه برای فعالیت های پژوهشی',
                                            max_length=20, blank=True,
                                            choices=[
                                                ('کامپیوتر', 'کامپیوتر'),
                                                ('رباتیک', 'رباتیک'),
                                                ('زیست', 'زیست'),
                                                ('شیمی', 'شیمی'),
                                                ('هنر و معماری', 'هنر و معماری'),
                                                ('هیچکدام', 'هیچکدام'),
                                            ],
                                        )
    shahed_in_all_schools = models.CharField(verbose_name='ویژه‌ی ثبت نام شاهد و ایثارگر',
                                                max_length=30, blank=True,
                                                choices=[
                                                    ('فرزند شهید', 'فرزند شهید'),
                                                    ('فرزند مفقودالاثر', 'فرزند مفقودالاثر'),
                                                    ('فرزند جانباز', 'فرزند جانباز'),
                                                ],
                                            )
    physical_situation = models.CharField(verbose_name='وضعیت جسمانی', max_length=30, blank=True,
                                            choices=[
                                                ('سالم', 'سالم'),
                                                ('دارای معلولیت', 'دارای معلولیت')
                                            ],
                                            default='سالم',
                                        )
    left_handed = models.CharField(verbose_name='چپ دست هستید؟', max_length=30, blank=False,
                                    choices=[
                                        ('بلی', 'بلی'),
                                        ('خیر', 'خیر'),
                                    ],
                                    default='خیر',
                                )

    #     مشخصات والدین
    father_edu = models.CharField(verbose_name='تحصیلات پدر', max_length=50, blank=False)
    father_job = models.CharField(verbose_name='شغل پدر', max_length=50, blank=False)
    father_job_place = models.TextField(verbose_name='آدرس محل کار پدر', max_length=200, blank=False)
    father_job_phone = models.CharField(verbose_name='تلفن محل کار پدر', max_length=11, blank=True,
                                        help_text="مثال: ۰۲۱۸۸۳۲۹۱۸۲",
                                        )
    mother_family = models.CharField(verbose_name='نام خانوادگی مادر', max_length=30, blank=False)
    mother_edu = models.CharField(verbose_name='تحصیلات مادر', max_length=50, blank=False)
    mother_job = models.CharField(verbose_name='شغل مادر', max_length=50, blank=False)
    mother_job_place = models.TextField(verbose_name='آدرس محل کار مادر', max_length=50, blank=True)
    mother_job_phone = models.CharField(verbose_name='تلفن محل کار مادر', max_length=11, blank=True, 
                                        help_text="مثال: ۰۲۱۸۸۳۲۹۱۸۲",
                                        )
    father_phone = models.CharField(verbose_name='شماره موبایل پدر', max_length=11, blank=False,
                                    help_text="مثال: ۰۹۱۲۳۴۵۶۷۸۹",
                                    )
    mother_phone = models.CharField(verbose_name='شماره موبایل مادر', max_length=11, blank=False,
                                    help_text="مثال: ۰۹۱۲۳۴۵۶۷۸۹")
    
    #     اطلاعات سکونت
    home_location = models.TextField(verbose_name='آدرس منزل', max_length=200, blank=False)
    home_postal_code = models.CharField(verbose_name='کدپستی منزل', max_length=11, blank=False,
                                        help_text="مثال: ۶۷۸۹۰-۱۲۳۴۵",
                                        )
    home_phone = models.CharField(verbose_name='تلفن منزل', max_length=11, blank=True,
                                    help_text="مثال: ۰۲۱۸۸۳۲۹۱۸۲",
                                )
    home_situation = models.CharField(verbose_name='وضعیت مسکن خانواده', max_length=30, blank=True,
                                        choices=[
                                            ('اجاره‌ای', 'اجاره‌ای'),
                                            ('شخصی', 'شخصی'),
                                            ('سازمانی', 'سازمانی'),
                                            ('سایر', 'سایر'),
                                        ],
                                    )
    homemate = models.CharField(verbose_name='در خانواده با چه کسانی زندگی می کنید؟',
                                max_length=30, blank=True,
                                choices=[
                                    ('پدر و مادر', 'پدر و مادر'),
                                    ('پدر و مادرخوانده', 'پدر و مادرخوانده'),
                                    ('مادر و پدرخوانده', 'مادر و پدرخوانده'),
                                    ('پدر', 'پدر'),
                                    ('مادر', 'مادر'),
                                    ('مادربزرگ و یا پدربزرگ', 'مادربزرگ و یا پدربزرگ'),
                                    ('سایر بستگان', 'سایر بستگان'),
                                ],
                                default='پدر و مادر',
                                )
    student_own_place = models.CharField(verbose_name='وضعیت مسکن دانش‌آموز در صورتی که برای تحصیل دور از خانواده زندگی می کند، چگونه است؟',
                                            max_length=30, blank=True,
                                            choices=[
                                                ('خوابگاه دانش‌آموزی', 'خوابگاه دانش‌آموزی'),
                                                ('مسکن اجاره‌ای', 'مسکن اجاره‌ای'),
                                                ('منزل بستگان', 'منزل بستگان'),
                                            ],
                                        )
    family_children_counter = models.IntegerField(verbose_name='تعداد فرزندان خانواده', blank=False)
    this_child_counter = models.IntegerField(verbose_name='چندمین فرزند خانواده هستید؟', blank=False)
    student_have_reading_room = models.BooleanField(verbose_name='دانش‌آموز اتاق مستقل برای مطالعه دارد؟', blank=True, null=True,
                                                    choices=[
                                                        (True, 'بلی'),
                                                        (False, 'خیر'),
                                                    ],
                                                    )

    date_added = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profilePic', default="/profilePic/default.png")
    phone = models.CharField(max_length=30, blank=True, null=True)
    grade = models.CharField(choices=[('10', 'پایه ی دهم'),
                                      ('11', 'پایه ی یازدهم'),
                                      ('12', 'پایه ی دوازدهم')], max_length=2, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    job_title = models.CharField(max_length=50, default='دانش آموز')
    description = models.CharField(max_length=150, blank=True)
    financial_problem = models.BooleanField(default=False)

    CHOICE = [
        ('math', 'ریاضی'),
        ('phys', 'فیزیک'),
        ('chem', 'شیمی'),
        ('bio', 'زیست'),
        ('comp', 'کامپیوتر'),
        ('eng', 'زبان'),
        ('far', 'فارسی'),
        ('other', 'سایر'),
    ]
    group = models.CharField(max_length=8, choices=CHOICE, blank=True, null=True)
    mom_number = models.CharField(max_length=30, blank=True, null=True)
    dad_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = (
            ("send_sms", "send_sms"),
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=False)
    subject = models.CharField(max_length=50, blank=True)
    body = models.TextField(max_length=500, blank=False)
    seen = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)
