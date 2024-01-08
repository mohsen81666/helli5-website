from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from loginApp import views

urlpatterns = [
    path('', views.profile, name='profile'),
    re_path(r'ورود/', views.login, name='login'),
    # by default login will redirect user to /accounts/profile
    re_path(r'خروج/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
