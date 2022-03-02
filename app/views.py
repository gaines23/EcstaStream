"""
Definition of views.
"""

from datetime import datetime, date, time
import json, requests
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView
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



env = environ.Env()
environ.Env.read_env()
tmdb_key = env('TMDB_API_KEY')
tmdb = TMDb()
tmdb.tmdb_key = tmdb_key

movie = Movie()
tv = TV()
series = Collection()
person = Person()

Imdb_URL = env('IMDB_URL')
URL_API = env('RAPID_API_KEY')

    
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html'
    )

#class MainSearch(TemplateView):
#    template_name = 'app/search_form.html'

def MainSearchResults(request):
    assert isinstance(request, HttpRequest)
    search = Search()
    movie_stream = movie.watch_providers
    
    search_request = request.GET.get("search")
    multi_search = search.multi({"query":{search_request}, "include_adult":"False", "region":"US"})

    movies = []
    tv_shows = []
    people = []

    for m in multi_search:
        if m.media_type == 'movie' and m.media_type != 'person' and m.media_type != 'tv':
            if m.id == movie.watch_providers(m.id).results['US']:
                break
            movies.append(m)    
        else:
            break
        continue

    for t in multi_search:
        if t.media_type == 'tv' and t.media_type != 'person' and t.media_type != 'movie':
            if t.id == tv.watch_providers(t.id).results['US']:
                break
            tv_shows.append(t)
        else:
            break
        continue

    for p in multi_search:
        if p.media_type == 'person':
            people.append(p)

    context = {
        'people':people,
        'tv_shows':tv_shows,
        'movies':movies,
    }

    return render(
        request,
        'app/search_results.html',
        context
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
    
    details = movie.details(movieid)
    streaming = movie.watch_providers(movieid)
    us_streaming = streaming.results['US']
    credits = details['credits']
    trailers = details['videos']
    
    mov_seriesID = details.belongs_to_collection['id']
    seriesid = series.details(mov_seriesID)
    
    runtime = details.runtime
    hours = runtime // 60
    minutes = runtime % 60
    hours_runtime = "{} hr {} min".format(hours, minutes)
    
    imdbid = details.imdb_id

    class ImdbAPI(object):
        url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

        moviestring = {"i":{imdbid} ,"type":"movie", "r":"json"}

        headers = {
            'x-rapidapi-host': Imdb_URL,
            'x-rapidapi-key': URL_API
        }

        mov_response = requests.request("GET", url, headers=headers, params=moviestring)
        movie_api = mov_response.json()

    r = ImdbAPI.movie_api

    smlrobj = []
    for result in details['similar']:
        smlrobj.append(result)

    context = {
        'details': details,
        'smlrobj': smlrobj,
        'imdbid':imdbid,
        'r':r,
        'trailers':trailers,
        'streaming':streaming,
        'credits':credits,
        'seriesid':seriesid,
        'us_streaming':us_streaming,
        'hours_runtime':hours_runtime,
    }

    return render(
        request,
        'movies/movie_details.html',
        context,
    )


def TvDetails(request, tvid):
    assert isinstance(request, HttpRequest)

    details = tv.details(tvid)
    streaming = tv.watch_providers(tvid)
    similar = details.similar
    trailers = details.videos
    credits = details.credits
    external_id = details.external_ids
    series = details.seasons
    
    imdbid = external_id.imdb_id
    us_streaming = streaming.results['US']

    class ShowImdbAPI(object):
        url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

        tvstring = {"i":{imdbid},"type":"series","r":"json"}

        headers = {
            'x-rapidapi-host': Imdb_URL,
            'x-rapidapi-key': URL_API
        }

        tv_response = requests.request("GET", url, headers=headers, params=tvstring)
        tv_api = tv_response.json()

    r = ShowImdbAPI.tv_api

    context = {
        'details': details,
        'imdbid':imdbid,
        'trailers':trailers,
        'streaming':streaming,
        'credits':credits,
        'us_streaming':us_streaming,
        'series':series,
        'r':r,
    }

    return render(
        request,
        'tvshows/tvdetails.html',
        context,
    )


def CreditsDetails(request, personid):
    assert isinstance(request, HttpRequest)
    
    details = person.details(personid)
    credits = details.combined_credits

    cast = credits.cast
    crew = credits.crew
    bday = datetime.strptime(details.birthday, '%Y-%m-%d').date().strftime('%B %d, %Y')
    
    bday_date = datetime.strptime(details.birthday, '%Y-%m-%d').date()
    today = date.today()

    one_or_zero = ((today.month, today.day) < (bday_date.month, bday_date.day))
    year_difference = today.year - bday_date.year
    age = year_difference - one_or_zero

    context = {
        'details':details,
        'credits':credits,
        'cast':cast,
        'crew':crew,
        'bday':bday,
        'age':age,
    }

    return render(
        request,
        'credits/creditsdetails.html',
        context,
    )