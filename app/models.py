from django.db import models
from django.contrib.auth.models import User
from datetime import date, time, datetime
from PIL import Image
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField


try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField


class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'app_collection'


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.genre

    class Meta:
        managed = False
        db_table = 'app_genre'

class StreamingRegion(models.Model):
    iso_3166_1 = models.CharField(primary_key=True, max_length=5)
    native_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_streamingregion'


class StreamingServices(models.Model):
    provider_id = models.IntegerField(primary_key=True)
    display_priority = models.IntegerField(blank=True, null=True)
    logo_path = models.CharField(max_length=200, blank=True, null=True)
    provider_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.provider_name

    class Meta:
        managed = False
        db_table = 'app_streamingservices'

## Age Ratings ##
class UsCerts(models.Model):
    us_certsid = models.AutoField(primary_key=True)
    certification = models.CharField(max_length=10, blank=True, null=True)
    meaning = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_uscerts'

class Streamingurls(models.Model):
    provider_id = models.IntegerField(primary_key=True)
    url_path = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_streamingurls'





class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profpic = models.ImageField(default='default.png', upload_to='profile_images', null=True)
    bio = models.TextField(null=True)
    streaming_services = models.ForeignKey(StreamingServices, on_delete=models.CASCADE, null=True)
    fav_genres = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profpic.path)
    
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.profpic.path)
            

class FavoriteListData(models.Model):
    mediaChoices = (
        (1,'Movie'),
        (2, 'TV')
    )

    favid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_mov_show_id = models.IntegerField()
    fav_date_added = models.DateTimeField(auto_now=True)
    media_type = models.IntegerField(null=True, blank=True, choices=mediaChoices)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "fav_mov_show_id", "media_type"], name='fav_constraint')    
        ]

class WatchListData(models.Model):
    mediaChoices = (
        (1,'Movie'),
        (2, 'TV')
    )

    watchid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch_mov_show_id = models.IntegerField()
    watch_date_added = models.DateTimeField(auto_now=True)
    media_type = models.IntegerField(null=True, blank=True, choices=mediaChoices)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "watch_mov_show_id", "media_type"], name='watchlist_constraint')    
        ]








class UserFavoritesList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favs_list = JSONField(default=list, null=True, blank=True)
### add user settings/preferences 

class UserWatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch_list = JSONField(default=list, null=True, blank=True)
### add user settings/preferences 


class MoviesList(models.Model):
    movieid = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=30)
    genre_list = JSONField(max_length=100)
    release_date = models.DateTimeField()
    poster_path = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.movieid + self.title









    
#     favorites = ArrayField(models.IntegerField(),null=True, blank=True, default=list)





#class Watchlist(models.Model):
#    id = models.AutoField(primary_key=True)
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    watch_movie_show_id = models.BigIntegerField()
#    share = models.BooleanField()
#    private = models.BooleanField()
#    date_added = models.DateTimeField(auto_now=True)
#    add_watch = models.ManyToManyField(User, related_name="addwatch", default=None)
#    watch_like = models.ManyToManyField(User, related_name='watchlike', default=None)
#    watch_like_count = models.BigIntegerField(default='0')

#    class Meta:
#        ordering = ['-date_added']

#    def __str__(self):
#       return 'WatchList'

#class FavoriteList(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    favorites = jsonfield.JSONField(null=True, blank=True, default={})

#    def __str__(self):
#        return self.user + 'favorite list'





#class FavoriteList(models.Model):
#    id = models.AutoField(primary_key=True)
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    #movie_show_id = models.BigIntegerField()
#    share = models.BooleanField()
#    private = models.BooleanField()
#    date_added = models.DateTimeField(auto_now=True)
#    favorites = JSONField(related_name="favorite", default=None)
#    user_likes = models.ManyToManyField(User, related_name='like', default=None)
#    user_fav_like_count = models.BigIntegerField(default='0')

#    class Meta:
#        ordering = ['-date_added']
    
#    def __str__(self):
#        return 'Favorites List'

#class Playlists(models.Model):
#    play_list_name = models.TextField(max_length=50)
#    id = models.AutoField(primary_key=True)
#    pl_movie_show_id = models.BigIntegerField()
#    created_by_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#    share = models.BooleanField()
#    private = models.BooleanField()
#    created_on = models.DateTimeField(auto_now=True)
#    updated_on = models.DateTimeField(auto_now=True)
#    playlist_favorites = models.ManyToManyField(User, related_name="favorite", default=None)
#    image_caption = models.CharField(max_length=100),
#    friends_like_playlist = models.ManyToManyField(User, related_name='like', default=None)
#    playlist_like_count = models.BigIntegerField(default='0')

#    def __str__(self):
#        return self.play_list_name + self.id












#class Movie(models.Model):
#    movieid = models.IntegerField(primary_key=True) # id
#    adult = models.BooleanField() # Need to Query Only FALSE
#    collection = models.OneToOneField(Collection, on_delete=models.CASCADE) ## Movie Series
#    budget = models.IntegerField()
#    genres = models.ForeignKey(Genre)
#    imdbid = models.IntegerField()
#    orginal_language = models.CharField(max_length=10)
#    title = models.CharField(max_length=100) # title NOT original title
#    summary = models.CharField(max_length=500) # overview
#    release_date = models.DateField()
#    revenue = models.IntegerField()
#    runtime = models.IntegerField()
#    tagline = models.CharField(max_length=200)
#    poster_path = models.CharField(max_length=200)
#    poster_img = models.ImageField(upload_to='poster_images', null=True)
#    age_rating = models.ForeignKey(UsCerts)
#    provider_id = models.ForeignKey(StreamingServices)
#    trailer = models.


    


#class Movie(models.Model):
#    movieid = models.IntegerField(primary_key=True)
#    year = models.IntegerField()
#    rank = models.IntegerField(blank=True, null=True)
#    title = models.CharField(max_length=30)
#    description = models.CharField(max_length=500, null=True)
#    duration = models.IntegerField(blank=True, null=True)
#    genres = models.CharField(max_length=100)
#    rating = models.FloatField(blank=True, null=True)
#    metascore = models.IntegerField(blank=True, null=True, default=None)
#    votes = models.IntegerField(blank=True, null=True)
#    gross_earning_in_mil = models.FloatField(blank=True, null=True, default=None)
#    director = models.ForeignKey('Director', related_name='+', on_delete=models.CASCADE, null=True, blank=True)
#    actor = models.ForeignKey('Actor', related_name='ActedBy+', on_delete=models.CASCADE, null=True, blank=True)

#class Director(models.Model):
#    name = models.CharField(max_length=100, primary_key=True)
#    date = models.CharField(max_length=100, null=True)
#    place = models.CharField(max_length=500, null=True)
#    masterpiece = models.CharField(max_length=500, null=True)
#    award_win = models.IntegerField(blank=True, null=True, default=None)
#    award_nom = models.IntegerField(blank=True, null=True, default=None)
#    person_link = models.URLField(max_length=500, null=True, default=None)
#    award_link = models.URLField(max_length=500, null=True, default=None)

#class Actor(models.Model):
#    name = models.CharField(max_length=100, primary_key=True)
#    date = models.CharField(max_length=100, null=True)
#    place = models.CharField(max_length=500, null=True)
#    masterpiece = models.CharField(max_length=500, null=True)
#    award_win = models.IntegerField(blank=True, null=True, default=None)
#    award_nom = models.IntegerField(blank=True, null=True, default=None)
#    person_link = models.URLField(max_length=500, null=True, default=None)
#    award_link = models.URLField(max_length=500, null=True, default=None)



