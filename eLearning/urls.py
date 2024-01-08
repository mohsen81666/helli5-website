from django.urls import path, re_path
from eLearning import views

urlpatterns = [
    path('', views.elearning_stuff, name='elearning_stuff'),
    re_path(r'حضورغیاب', views.check_classes, name='check_classes'),
]
