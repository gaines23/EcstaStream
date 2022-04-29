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
    path('friend/<id>/<username>', views.FriendProfile, name='friends-profile'),
    path('send_follower_request/<int:userid>/', views.send_follower_request, name='send-follow-request'),
    path('accept_follower_request/<int:requestid>/', views.accept_follower_request, name='accept-follow-request'),
    path('reject_follower_request/<int:requestid>/', views.reject_follower_request, name='reject-follow-request'),
    path('follow/<id>/<username>', views.add_follower, name='follow'),
    path('unfollow/<id>/<username>', views.remove_follower, name='unfollow'),
    path('create-playlist/<user>/', views.CreatePlaylist, name='user_create_playlist'),
    path('playlist/<user>/<title>', views.user_playlist, name='user_playlist'),
    path('edit-playlist/<user>/<title>', views.edit_user_playlist, name='edit_playlist'),
    path('favorites', views.favorites_list, name='fav-list'),
    path('watchlist', views.watch_list, name='watchlist'),
    path('MovieDetails/<movieid>/<media_type>', views.MovieDetails, name='MovieDetails'),
    path('fav-movie/<movieid>/<media_type>', views.favorite_add_movie, name='fav-add-movie'),
    path('watchlist-movie/<int:movieid>/<media_type>', views.watchlist_add_movie, name='watchlist-add-movie'),
    path('add-movie-to-playlist/<user>/<user_playlist_id>/<int:movieid>/<media_type>', views.playlist_add_movie, name='playlist-add-movie'),
    path('TvDetails/<tvid>/<media_type>', views.TvDetails, name='TvDetails'),
    path('add-tv-to-playlist/<user>/<user_playlist_id>/<int:tvid>/<media_type>', views.playlist_add_tv, name='playlist-add-tv'),
    path('fav-show/<tvid>/<media_type>', views.favorite_add_tv, name='fav-add-tv'),
    path('watchlist-show/<int:tvid>/<media_type>', views.watchlist_add_tv, name='watchlist-add-tv'),
    path('CreditsDetails/<personid>', views.CreditsDetails, name='CreditsDetails'),
    path('register/', RegisterView.as_view(), name='users-register'),
]
