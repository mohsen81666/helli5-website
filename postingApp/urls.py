from django.urls import path, re_path, include
from .views import *

urlpatterns = [

    path('', blog, name='blog'),
    path('تگ/<tag>', blog, name='blog'),
    # path('add_post_teacher/', add_post_teacher, name='add_post_teacher'),
    # path('add_post/', add_post, name='add_post'),
    path('جستجو/', search, name='search'),
    # path('tag_res/<id>/', posts_by_cat, name='tag_res'),
    re_path(r'^(?P<slug>[\w-]+)/$', blog_single, name='blog_single'),
    # url(r'^(?P<slug>[\w-]+)/update/$', blog_update, name='blog_update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', blog_delete, name='blog_delete'),
    path('events', events, name='events'),

]
