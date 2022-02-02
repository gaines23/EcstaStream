from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import *

admin.site.register(Profile)

admin.site.register(Genre)
admin.site.register(StreamingProviders)
admin.site.register(StreamingRegion)
admin.site.register(Collection)
admin.site.register(Movie)

#admin.site.register(Movie)
#admin.site.register(Director)
#admin.site.register(Actor)