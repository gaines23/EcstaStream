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
    path('MovieDetails/<movieid>', views.MovieDetails, name='MovieDetails'),
    path('fav-movie/<movieid>/<media_type>', views.favorite_add_movie, name='fav-add-movie'),
    path('TvDetails/<tvid>', views.TvDetails, name='TvDetails'),
    path('watchlist-movie/<int:movieid>/<media_type>', views.watchlist_add_movie, name='watchlist-add-movie'),
    path('fav-show/<tvid>/<media_type>', views.favorite_add_tv, name='fav-add-tv'),
    path('watchlist-show/<int:tvid>/<media_type>', views.watchlist_add_tv, name='watchlist-add-tv'),
    path('favorites', views.favorites_list, name='fav-list'),
    path('watchlist', views.watch_list, name='watchlist'),
    path('CreditsDetails/<personid>', views.CreditsDetails, name='CreditsDetails'),
    path('register/', RegisterView.as_view(), name='users-register'),
]