from django.db import models
from django.contrib.auth.models import User
from datetime import date, time, datetime
from PIL import Image
from multiselectfield import MultiSelectField

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.png', upload_to='profile_images', null=True)
    bio = models.TextField(null=True)
    #posts = models.OneToManyField(Post) # id = 

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
    
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)



## 

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

    class Meta:
        managed = False
        db_table = 'app_streamingservices'

## Age Ratings
class UsCerts(models.Model):
    us_certsid = models.AutoField(primary_key=True)
    certification = models.CharField(max_length=10, blank=True, null=True)
    meaning = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_uscerts'

#class Movie(models.Model):
#    movieid = models.IntegerField(primary_key=True) # id
#    adult = models.BooleanField() # Need to Query Only FALSE
#    collection = models.OneToOneField(Collection, on_delete=models.CASCADE) ## Movie Series
#    budget = models.IntegerField()
#    #genres = models.ForeignKey(Genre)
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
#    age_rating = models.CharField(max_length=10)




    


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



