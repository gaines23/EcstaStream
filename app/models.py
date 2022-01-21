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




