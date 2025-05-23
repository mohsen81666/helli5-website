"""helli5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from . import views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from postingApp.feeds import LatestPostsFeed
from loginApp.views import pre_registeration
from loginApp.views import export_pre_registrations
from pansouqApp.views import students_list

handler400 = views.custom_400
handler403 = views.custom_403
handler404 = views.custom_404
handler500 = views.custom_500

urlpatterns = [

    path('', views.index, name='index'),
    path('export-pres/', export_pre_registrations, name='export-pres'),
    path('export-pres/<year>', export_pre_registrations, name='export-pres-current'),

    path('admin/', admin.site.urls),
    path('feed/rss', LatestPostsFeed(), name='posts_feed'),
    path('ارتباط-با-ما/', views.contact, name='contact'),
    path('درباره-ما/', views.about, name='about'),
    path('کنکور/', views.konkour, name='konkour'),
    path('teachers/', views.teachers, name='teachers'),

    path('pre-registeration/', pre_registeration, name='pre_registeration'),
    path('pre-registeration/<melli>/<ssid>', pre_registeration, name='compelete_pre_registeration'),
    path('students_list/<challenge_id>/', students_list, name='pansouq_students'),
    # path('error503/', views.error503, name='error503'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    re_path(r'^accounts/', include('loginApp.urls')),
    re_path(r'^posts/', include('postingApp.urls')),
    re_path(r'^افتخارات/', include('honorsApp.urls')),
    re_path(r'panel/', include('smsApp.urls')),
    re_path(r'^courses/', include('courseApp.urls')),
    re_path(r'^elearning/', include('eLearning.urls', namespace='eLearning')),
    re_path(r'^پژوهشی/', include('pansouqApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
