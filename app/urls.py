from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from app.forms import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<id>/<username>', views.profile, name='users-profile'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('TitlePage/<int:id>', views.TitlePage, name='TitlePage'),
]