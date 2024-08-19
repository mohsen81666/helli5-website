from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from loginApp import views

urlpatterns = [
    path('', views.user_panel, name='user-panel'),
    re_path(r'login/', views.login, name='login'),
    re_path(r'set-own-password/', views.set_own_password, name='set-own-password'),
    re_path(r'set-onetimeentry-password/', views.set_oneTimeEntry_password, name='set-oneTimeEntry-password'),
    re_path(r'logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
