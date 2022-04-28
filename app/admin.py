from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import *

admin.site.register(Profile)
admin.site.register(FavoriteListData)
admin.site.register(UserFavoritesList)
admin.site.register(WatchListData)
admin.site.register(UserWatchList)
admin.site.register(MoviesList)
admin.site.register(Genre)
admin.site.register(StreamingServices)
admin.site.register(StreamingRegion)
admin.site.register(Collection)
admin.site.register(UsCerts)
admin.site.register(Streamingurls)
admin.site.register(UserPlaylistPost)
admin.site.register(UserPlaylist)
admin.site.register(UserPlaylistData)
admin.site.register(FollowRequest)
admin.site.register(Comment)
admin.site.register(UserStatusPost)


#admin.site.register(Movie)
#admin.site.register(Watchlist)

#admin.site.register(Playlists)
#admin.site.register(Movie)
#admin.site.register(Director)
#admin.site.register(Actor)