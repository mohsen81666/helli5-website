from django.urls import path, re_path
from .views import *

urlpatterns = [

    path('<pansouq_id>/', pansouq, name='pansouq'),
    # re_path(r'^(?P<slug>[\w-]+)/update/$', blog_update, name='blog_update'),
]
