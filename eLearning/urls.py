from django.urls import path, re_path
from eLearning import views

app_name = 'eLearning'

urlpatterns = [
    path('', views.elearning, name='elearning'),
    re_path(r'check-online-classes', views.check_online_classes, name='check_online_classes'),
]
