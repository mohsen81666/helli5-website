from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect
import xlwt
from helli5.decorators import unauth_user
from .models import PreRegisteredStudent, SetOwnPassword
from .forms import LoginForm, SignUpForm, SetOwnPasswordForm, SetOneTimeEntryPassword, PreRegisterationFrom

@login_required(login_url='login')
def user_panel(request):
    # user = request.user

    context = {}
    return render(request, 'profile.html', context)


@csrf_protect
@unauth_user
def pre_registeration(request, melli=None, ssid=None):
    url = None
    form = PreRegisterationFrom()
    if melli is not None and ssid is not None:
        try:
            form = PreRegisterationFrom(instance=PreRegisteredStudent.objects.get(melli_code=melli, ss_id=ssid))
        except ObjectDoesNotExist:
            messages.warning(request, 'چنین فرمی قبلاً پر نشده است.')
    elif request.method == 'POST':
        form = PreRegisterationFrom(request.POST)
        if form.is_valid():
            try:
                PreRegisteredStudent.objects.get(melli_code=form.cleaned_data['melli_code']).delete()
            except ObjectDoesNotExist:
                pass
            finally:
                obj = form.save(commit=False)
                obj.is_valid = True
                obj.save()
                # TODO: URL should be independent from domain
                url = "http://" + settings.SITE_URL +  "/pre-registeration/" + form.cleaned_data['melli_code'] + "/" + form.cleaned_data['ss_id']
                messages.success(request, 'مشخصات وارد شده در سامانه ثبت شد و برای پیگیری منتظر اطلاعیه‌های بعدی باشید.')
                messages.success(request, 'برای تغییر اطلاعات فرم پیش ثبت نام می توانید از لینک زیر استفاده کنید. این لینک را برای استفاده های بعدی در جایی یادداشت کنید یا آن را در مرورگر خود نشانگذاری(bookmark) کنید.')
        else:
            messages.warning(request, 'متاسفانه اطلاعات وارد شده معتبر نبوده و در سامانه ثبت نشد')

    context = {
        'pre_registeration_form': form,
        'complete_url': url
    }
    return render(request, 'pre_registeration.html', context)


@csrf_protect
@unauth_user
def login(request):
    login_form, signup_form = None, None
    if request.method == "POST":

        if request.POST.get('submit') == 'ورود':
            login_form = LoginForm(request.POST or None)
            if login_form.is_valid():
                # get authenticated user
                user = login_form.login(request)

                # Check if user changed his one time entry password and if not, redirect him to set password
                try:
                    set_own_password = SetOwnPassword.objects.get(user=user)
                except SetOwnPassword.DoesNotExist:
                    set_own_password = None
                if not(set_own_password and set_own_password.is_set):
                    request.session['username'] = user.username
                    return redirect('set-own-password')

                if user:
                    # login user and redirect to panel
                    auth_login(request, user)
                    return redirect('user-panel')

        elif request.POST.get('submit') == 'ثبت نام':
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.profile.birth_date = signup_form.cleaned_data.get('birth_date')
                user.profile.phone = signup_form.cleaned_data.get('phone')
                # user.profile.img = request.POST['img']
                user.save()
                raw_password = signup_form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                print(user)
                auth_login(request, user)
                return redirect('index')

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }
    return render(request, 'login.html', context)


@csrf_protect
@unauth_user
def set_own_password(request):
    set_password_form = SetOwnPasswordForm(request.POST or None)
    if request.method == "POST":
        username = request.session.get('username')
        if set_password_form.is_valid():
            raw_password1 = set_password_form.cleaned_data.get('password1')
            raw_password2 = set_password_form.cleaned_data.get('password2')
            if raw_password1 == raw_password2:
                user = User.objects.get(username=username)
                user.set_password(raw_password1)
                user.save()
                try:
                    set_own_password = SetOwnPassword.objects.get(user=user)
                except SetOwnPassword.DoesNotExist:
                    set_own_password = SetOwnPassword(user=user, is_set=False)
                set_own_password.is_set = True
                set_own_password.save()
            return redirect('login')

    return render(request, 'set_own_password.html', context={'set_password': set_password_form})


@csrf_protect
def set_oneTimeEntry_password(request):
    user = request.user
    if user.is_authenticated and user.username == 'admin':
        set_password_form = SetOneTimeEntryPassword(request.POST or None)
        if request.method == "POST":
            if set_password_form.is_valid():
                username = set_password_form.cleaned_data.get('username')
                raw_password = set_password_form.cleaned_data.get('password')
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    set_password_form.errors['error'] = 'کاربر یافت نشد.'
                    return render(request, 'set_oneTimeEntry_password.html', context={'set_password_form': set_password_form})
                user.set_password(raw_password)
                user.save()
                set_own_password = SetOwnPassword.objects.get(user=user)
                set_own_password.is_set = False
                set_own_password.save()

                return redirect('user-panel')

    return render(request, 'set_oneTimeEntry_password.html', context={'set_password_form': set_password_form})


def export_pre_registrations(request, year=None):
    user = request.user
    if user.is_authenticated and user.username == 'admin':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['نام', 'نام خانوادگی', 'نام پدر', 'روز تولد', 'ماه تولد', 'سال تولد',
                   'کد ملی', 'سریال ۶رقمی شناسنامه', 'سری حروفی ش.', 'سری عددی ش.',
                   'محل صدور', 'استان تولد', 'شهرستان تولد', 'دین', 'ملیت',
                   'موبایل دانش آموز', 'ایمیل دانش آموز',
                   'معدل کل پایه نهم', 'نام مدرسه‌ی قبلی', 
                   'رشته‌ی تحصیلی', 'المپیادهای علمی', 'زمینه‌ی پژوهشی', 
                   'ویژه ی ثبت نام شاهد', 'وضعیت جسمانی', 'چپ دست',
                   'تحصیلات پدر', 'شغل پدر', 'آدرس محل کار پدر', 'تلفن محل کار پدر',
                   'نام خانوادگی مادر', 'تحصیلات مادر', 'شغل مادر', 'آدرس محل کار مادر', 'تلفن محل کار مادر',
                   'شماره موبایل پدر', 'شماره موبایل مادر',
                   'آدرس منزل', 'کدپستی', 'تلفن منزل', 'وضعیت مسکن خانواده',
                   'در خانواده با چه کسانی زندگی می کنید؟',
                   'وضعیت مسکن دانش آموز در صورتی که برای تحصیل دور از خانواده زندگی می کند، چگونه است؟',
                   'تعداد فرزندان خانواده', 'چندمین فرزند خانواده',
                   'دانش آموز اتاق مستقل برای مطالعه دارد؟',
                   ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        if year is None:
            rows = PreRegisteredStudent.objects.all()
        else:
            rows = PreRegisteredStudent.objects.filter(date_added__year=year)

        for row in rows:
            row_num += 1
            ws.write(row_num, 0, row.student_first_name, font_style)
            ws.write(row_num, 1, row.student_last_name, font_style)
            ws.write(row_num, 2, row.father_first_name, font_style)
            ws.write(row_num, 3, row.birth_day, font_style)
            ws.write(row_num, 4, row.birth_month, font_style)
            ws.write(row_num, 5, row.birth_year, font_style)
            ws.write(row_num, 6, row.melli_code, font_style)
            ws.write(row_num, 7, row.ss_id, font_style)
            ws.write(row_num, 8, row.ss_alphabetical, font_style)
            ws.write(row_num, 9, row.ss_numerical, font_style)
            ws.write(row_num, 10, row.export_place, font_style)
            ws.write(row_num, 11, row.birth_place_state, font_style)
            ws.write(row_num, 12, row.birth_place_town, font_style)
            ws.write(row_num, 13, row.religion, font_style)
            ws.write(row_num, 14, row.nationality, font_style)
            ws.write(row_num, 15, row.student_phone, font_style)
            ws.write(row_num, 16, row.student_mail, font_style)
            ws.write(row_num, 17, row.grade_at_9th, font_style)
            ws.write(row_num, 18, row.last_year_school_name, font_style)
            ws.write(row_num, 19, row.field_of_study, font_style)
            ws.write(row_num, 20, row.field_of_olympiad, font_style)
            ws.write(row_num, 21, row.field_of_pajohesh, font_style)
            ws.write(row_num, 22, row.shahed_in_all_schools, font_style)
            ws.write(row_num, 23, row.physical_situation, font_style)
            ws.write(row_num, 24, row.left_handed, font_style)

            ws.write(row_num, 25, row.father_edu, font_style)
            ws.write(row_num, 26, row.father_job, font_style)
            ws.write(row_num, 27, row.father_job_place, font_style)
            ws.write(row_num, 28, row.father_job_phone, font_style)
            ws.write(row_num, 29, row.mother_family, font_style)
            ws.write(row_num, 30, row.mother_edu, font_style)
            ws.write(row_num, 31, row.mother_job, font_style)
            ws.write(row_num, 32, row.mother_job_place, font_style)
            ws.write(row_num, 33, row.mother_job_phone, font_style)
            ws.write(row_num, 34, row.father_phone, font_style)
            ws.write(row_num, 35, row.mother_phone, font_style)
            ws.write(row_num, 36, row.home_location, font_style)
            ws.write(row_num, 37, row.home_postal_code, font_style)
            ws.write(row_num, 38, row.home_phone, font_style)
            ws.write(row_num, 39, row.home_situation, font_style)

            ws.write(row_num, 40, row.homemate, font_style)
            ws.write(row_num, 41, row.student_own_place, font_style)
            ws.write(row_num, 42, row.family_children_counter, font_style)
            ws.write(row_num, 43, row.this_child_counter, font_style)
            ws.write(row_num, 44, row.student_have_reading_room, font_style)

        wb.save(response)
        return response

    template = loader.get_template('401.html')
    return HttpResponse(template.render({}, request))
