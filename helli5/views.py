from django.shortcuts import render, redirect
from django.http import HttpResponse
from helli5 import settings
from .models import *
from .forms import *
from postingApp.models import PostStuff, Event
from loginApp.models import Contact, TeacherProfile, TeachingDepartment
from django.db.models import Q
from dynamicApp.models import SliderContent
from loginApp.forms import ContactForm
import os
import xlwt
import jdatetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


def index(request):
    # TODO: uncomment subscribe form
    # if request.method == "POST":
    #     if request.POST.get('submit') == 'عضویت':
    #         try:
    #             email = request.POST["email"]
    #             new_subscriber = Subscriber()
    #             new_subscriber.email = email
    #             new_subscriber.save()
    #         except Exception:
    #             pass
    slider_contents = SliderContent.objects.filter(Q(visible=True)).order_by('-date')[0:6]
    latest = PostStuff.objects.order_by('-date')[0:6]
    events = Event.objects.filter(date__gte=jdatetime.date.today()).order_by('date')
    context = {
        'latest_posts': latest,
        'events': events,
        'slider_contents': slider_contents
    }
    return render(request, 'index.html', context)

def elearning(request):
    context = {
        'moodle_url': 'https://lms.' + settings.SITE_URL,
        'telegram_url': 'https://t.me/allamehelli5',
        'aparat_url': 'https://www.aparat.com/allamehelli5',
    }
    return render(request, 'elearning.html', context)

# def footer(request):
#     events = Event.objects.order_by('-date')[0:6]
#     context = {
#         'events': events,
#     }
#     return render(request, 'footer.html', context)


def contact(request):
    status = 0
    if request.method == 'POST':
        if request.POST.get('form-key') == 'ارتباط-با-ما':
            status = -1
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                try:
                    contact_obj = Contact(
                        name=contact_form.cleaned_data['name'],
                        email=contact_form.cleaned_data['email'],
                        subject=contact_form.cleaned_data['subject'],
                        body=contact_form.cleaned_data['body'])
                    contact_obj.save()
                    status = 1
                except:
                    pass

    context = {
        'contact_form': ContactForm(),
        'status': status
    }
    return render(request, 'contact.html', context)


def about(request):
    return render(request, 'about.html', {})


def teachers(request):
    departments = TeachingDepartment.objects.all().order_by('order')
    profiles = TeacherProfile.objects.filter(Q(active=True) & Q(promote=True))

    groups = {}
    for department in departments:
        groups[department.name] = [p for p in profiles if p.department == department]

    context = {
        'groups': groups,
    }
    return render(request, 'teachers.html', context)


def custom_400(request, exception):
    return render(request, '400.html', status=400)


def custom_403(request, exception):
    return render(request, '401.html', status=403)


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def konkour(request):
    return render(request, 'konkour.html')
