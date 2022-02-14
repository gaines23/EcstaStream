"""
Definition of views.
"""

from datetime import datetime
import json, requests
from django.contrib import messages
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.template import loader, Context
from django.views import generic
from django.http import HttpRequest
from .models import *
from .forms import *
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.forms.widgets import *
from django.db.models import Count
from django.forms import ModelForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, F
from .filter import *
from django.contrib.admin.views.decorators import staff_member_required
from tmdbv3api import *
import os
import environ
from django.db.models.functions import ExtractYear
from tmdbv3api.tmdb import TMDb
#from .rapidapi import ImdbRapiApi



env = environ.Env()
environ.Env.read_env()
tmdb_key = env('TMDB_API_KEY')
tmdb = TMDb()
tmdb.tmdb_key = tmdb_key

movie = Movie()
tv = TV()
discover = Discover()
series = Collection()



def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html'
    )




## LOGIN/LOGOUT ##

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


class NewLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(NewLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We have emailed you instructions for resetting your password. " \
                     "Please contact support if you did not receive the password " \
                     "reset email."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')



@login_required
def profile(request, id, username):
    assert isinstance(request, HttpRequest)

    model = User
    userid = User.objects.get(id=id)

    model = Profile
    profid = Profile.objects.get(id=id)

    #new = Post.objects.filter(favorites=request.user)

    if request.method == 'POST' and 'edit' in request.POST:
        user_form = UpdateUserForm(request.POST, instance=userid)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profid)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has updated successfully')
            return HttpResponseRedirect("/profile/"+id+"/"+username)
        else:
            user_form = UpdateUserForm(instance=userid)
            profile_form = UpdateProfileForm(instance=profid)
    else:
        user_form = UpdateUserForm(instance=userid)
        profile_form = UpdateProfileForm(instance=profid)

    context = {
            'userid': userid,
            'profid': profid,
            'user_form': user_form, 
            'profile_form': profile_form,
            #'new': new,
        }

    return render(request, 
                  'users/UserProfile.html',
                  context,
    )



#Don’t forget to add <span class="pre">.env</span> in your 
#<span class="pre">.gitignore</span> also, it’s advisable to create a 
#.env.example with a template of all the variables required for the project.

def MovieDetails(request, movieid):
    assert isinstance(request, HttpRequest)
    
    movobj = movie.details(movieid)
    similar = movie.similar(movieid)
    trailers = movie.videos(movieid)
    providers = movie.watch_providers(movieid)
    #movdis = discover.discover_movies
    credits = movie.credits(movieid)
    streaming = movie.watch_providers(movieid)
    

    imdbid = movobj.imdb_id

    class ImdbRapidApi(object):
        url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
        querystring = {"i":{imdbid},"type":"movie","r":"json"}

        Imdb_URL = "movie-database-imdb-alternative.p.rapidapi.com"
        URL_API = "93f4b600aemshd9c2d876469f714p1c0cb3jsn18656827b06a"

        headers = {
            'x-rapidapi-host': Imdb_URL,
            'x-rapidapi-key': URL_API
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        api = response.json()

    rapidapi = ImdbRapidApi()
    r = rapidapi.api

    us_streaming = streaming.results['US']

    cast = credits.cast['known_for_department'=='Acting']
    
    mov_seriesID = movobj.belongs_to_collection['id']
    seriesid = series.details(mov_seriesID)


    smlrobj = []
    for result in similar:
        smlrobj.append(result)

    context = {
        'movobj': movobj,
        'smlrobj': smlrobj,
        #'dis':movdis,
        'r':r,
        'trailers':trailers,
        'providers':providers,
        'credits':credits,
        'cast':cast,
        'seriesid':seriesid,
        'us_streaming':us_streaming,
    }

    return render(
        request,
        'movies/movie_details.html',
        context,
    )


