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



