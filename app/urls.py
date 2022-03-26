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
    path('MainSearchResults', views.MainSearchResults, name='search-results'),
    path('profile/<id>/<username>', views.profile, name='users-profile'),
    path('bookmarks/<int:id>/', views.favorite_add, name='fav-add'),
    #path('watchlist/', views.watchlist_list, name='watch-list'),
    path('favorites/', views.favorites_list, name='fav-list'),
    #path('like/', views.like, name='like'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('MovieDetails/<movieid>', views.MovieDetails, name='MovieDetails'),
    path('TvDetails/<tvid>', views.TvDetails, name='TvDetails'),
    path('CreditsDetails/<personid>', views.CreditsDetails, name='CreditsDetails'),
]