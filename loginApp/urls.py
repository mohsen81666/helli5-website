from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from loginApp import views

urlpatterns = [
    url(r'login/', views.login, name='login'),
    # by default login will redirect user to /accounts/profile
    url(r'logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
