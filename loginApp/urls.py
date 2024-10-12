from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', user_panel, name='user-panel'),
    re_path(r'login/', login, name='login'),
    re_path(r'set-own-password/', set_own_password, name='set-own-password'),
    re_path(r'change-user-password/', change_user_password, name='change-user-password'),
    re_path(r'bunch-add/', bunch_add, name='user-bunch-add'),
    re_path(r'logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
