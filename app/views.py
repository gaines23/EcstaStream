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
from .filters import *
from django.contrib.admin.views.decorators import staff_member_required
from tmdbv3api import *
import os
import environ
from django.db.models.functions import ExtractYear
from tmdbv3api.tmdb import TMDb
from django.contrib.auth.models import User
from friendship.models import Block, Follow, Friend, FriendshipRequest


try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User

env = environ.Env()
environ.Env.read_env()
tmdb_key = env('TMDB_API_KEY')
tmdb = TMDb()
tmdb.tmdb_key = tmdb_key

movie = Movie()
tv = TV()
series = Collection()
person = Person()
search = Search()

Imdb_URL = env('IMDB_URL')
URL_API = env('RAPID_API_KEY')



def home(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/index.html',
    )

@login_required
def SocialContent(request, username):
    assert isinstance(request, HttpRequest)

    """ View the friends of a user """
    user = get_object_or_404(user_model, username=username)
    friends = Friend.objects.friends(user)

    context = {
        'friends':friends,
    }

    return render(
        request,
        'app/social_content.html',
        context,
    )


def MainSearchResults(request):
    assert isinstance(request, HttpRequest)
    
    search_request = request.GET.get("search")
    multi_search = search.multi({"query":{search_request}, "include_adult":"False", "region":"US"})
    streaming_mov = movie.watch_providers
    streaming_tv = tv.watch_providers
    
    movies = []
    tv_shows = []
    people = []
 
    try:
        for m in multi_search:
            if m.media_type == 'movie' and m.media_type != 'person' and m.media_type != 'tv':
                if m.id == streaming_mov(m.id).results['US']:
                    break
                movies.append([m, streaming_mov(m.id).results['US']])
            else:
                break
            continue
    except Exception as e:
        print(e)

    try:
        for t in multi_search:
            if t.media_type == 'tv' and t.media_type != 'person' and t.media_type != 'movie':
                if t.id == streaming_tv(t.id).results['US']:
                    break    
                tv_shows.append([t, streaming_tv(t.id).results['US']])
            else:
                break
            continue
    except Exception as e:
        print(e)

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
    profid = Profile.objects.get(user=id)

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
        }

    return render(request, 
                  'users/UserProfile.html',
                  context,
    )






@login_required
def favorite_add_movie(request, movieid, media_type=1):
    assert isinstance(request, HttpRequest)

    fav_model = FavoriteListData.objects.all()

    if fav_model.filter(Q(user=request.user) & Q(fav_mov_show_id=movieid) & Q(media_type=1)).exists():
        fav_model.filter(Q(fav_mov_show_id=movieid) & Q(user=request.user) & Q(media_type=1)).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        fav_model.create(user=request.user, fav_mov_show_id=movieid, media_type=1)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def favorite_add_tv(request, tvid, media_type=2):
    assert isinstance(request, HttpRequest)

    fav_model = FavoriteListData.objects.all()

    if fav_model.filter(Q(user=request.user) & Q(fav_mov_show_id=tvid) & Q(media_type=2)).exists():
        fav_model.filter(Q(fav_mov_show_id=tvid) & Q(user=request.user) & Q(media_type=2)).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        fav_model.create(user=request.user, fav_mov_show_id=tvid, media_type=2)
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 
 

@login_required
def favorites_list(request):
    assert isinstance(request, HttpRequest)

    fav_list = list(FavoriteListData.objects.filter(Q(user=request.user)))
    favs = list(sorted(fav_list, key = lambda x: x.fav_date_added, reverse=True))
    all_favs = FavoriteListData.objects.all()

    details = []

    try:
        for x in favs:
            id = x.fav_mov_show_id
            media = x.media_type
            if x.media_type == 1:
                details.append([{'movie': movie.details(id)}, movie.watch_providers(id).results['US']])
            else:
                details.append([{'tv': tv.details(id)}, tv.watch_providers(id).results['US']])
    except Exception as e:
        pass
    
    context = {'favs':favs,
               'fav_list':fav_list,
               'details':details,
               'all_favs':all_favs,
    }

    return render(request,
                  'playlists/favorite_list.html',
                  context
    )













@login_required
def watchlist_add_movie(request, movieid, media_type=1):
    assert isinstance(request, HttpRequest)

    fav_model = WatchListData.objects.all()

    if fav_model.filter(Q(user=request.user) & Q(watch_mov_show_id=movieid) & Q(media_type=1)).exists():
        fav_model.filter(Q(watch_mov_show_id=movieid) & Q(user=request.user) & Q(media_type=1)).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        fav_model.create(user=request.user, watch_mov_show_id=movieid, media_type=1)
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 


@login_required
def watchlist_add_tv(request, tvid, media_type=2):
    assert isinstance(request, HttpRequest)

    fav_model = WatchListData.objects.all()

    if fav_model.filter(Q(user=request.user) & Q(watch_mov_show_id=tvid) & Q(media_type=2)).exists():
        fav_model.filter(Q(watch_mov_show_id=tvid) & Q(user=request.user) & Q(media_type=2)).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        fav_model.create(user=request.user, watch_mov_show_id=tvid, media_type=2)
        return HttpResponseRedirect(request.META['HTTP_REFERER']) 
 

@login_required
def watch_list(request):
    assert isinstance(request, HttpRequest)

    watch_list = list(WatchListData.objects.filter(Q(user=request.user)))
    watch = list(sorted(watch_list, key = lambda x: x.watch_date_added, reverse=True))
    all_watch = WatchListData.objects.all()

    details = []

    try:
        for x in watch:
            id = x.watch_mov_show_id
            media = x.media_type
            if x.media_type == 1:
                details.append([{'movie': movie.details(id)}, movie.watch_providers(id).results['US']])
            else:
                details.append([{'tv': tv.details(id)}, tv.watch_providers(id).results['US']])
    except Exception as e:
        pass
    
    context = {'watch':watch,
               'watch_list':watch_list,
               'details':details,
               'all_watch':all_watch,
    }

    return render(request,
                  'playlists/watchlist.html',
                  context
    )







## RATINGS Not Likes 

#@login_required
#def like(request):
#    if request.POST.get('action') == 'movie_show':
#        result = ''
#        id = int(request.POST.get('pl_movie_show_id'))
#        playlist = get_object_or_404(Post, id=id)

#        if playlist.likes.filter(id=request.user.id).exists():
#            playlist.likes.remove(request.user)
#            playlist.like_count -= 1
#            result = playlist.like_count
#            playlist.save()
#        else:
#            playlist.likes.add(request.user)
#            playlist.like_count += 1
#            result = playlist.like_count
#            playlist.save()

#        return JsonResponse({'result': result, })



#Don’t forget to add <span class="pre">.env</span> in your 
#<span class="pre">.gitignore</span> also, it’s advisable to create a 
#.env.example with a template of all the variables required for the project.


def MovieDetails(request, movieid, media_type=1):
    assert isinstance(request, HttpRequest)

    details = movie.details(movieid)
    streaming = movie.watch_providers(movieid)
    us_streaming = streaming.results['US']
    credits = details['credits']
    trailers = details['videos']
    
    favorited = FavoriteListData.objects.all()
    fav = bool

    if favorited.filter(Q(fav_mov_show_id=movieid) & Q(media_type=1)).exists():
        fav = True

    watchlist = WatchListData.objects.all()
    watch = bool

    if watchlist.filter(Q(watch_mov_show_id=movieid) & Q(media_type=1)).exists():
        watch = True

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

    mov_series = []

    try:
        mov_series.append(series.details(details.belongs_to_collection['id'])['parts'])
    except Exception as e:
        pass


    context = {
        'details': details,
        'smlrobj': smlrobj,
        'imdbid':imdbid,
        'r':r,
        'trailers':trailers,
        'streaming':streaming,
        'credits':credits,
        'mov_series':mov_series,
        'us_streaming':us_streaming,
        'hours_runtime':hours_runtime,
        'fav':fav,
        'watch':watch,
    }

    return render(
        request,
        'movies/movie_details.html',
        context,
    )


def TvDetails(request, tvid, media_type=2):
    assert isinstance(request, HttpRequest)

    details = tv.details(tvid)
    tv_title = details.name
    streaming = tv.watch_providers(tvid)
    similar = details.similar
    trailers = details.videos
    credits = details.credits
    external_id = details.external_ids

    favorited = FavoriteListData.objects.all()
    fav = bool

    if favorited.filter(Q(fav_mov_show_id=tvid) & Q(media_type=2)).exists():
        fav = True

    watchlist = WatchListData.objects.all()
    watch = bool

    if watchlist.filter(Q(watch_mov_show_id=tvid) & Q(media_type=2)).exists():
        watch = True

    tv_series = []

    try:
        tv_series.append(details.seasons)
    except Exception as e:
        pass
    
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
        'tv_series':tv_series,
        'r':r,
        'fav':fav,
        'watch':watch,
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
    movie_credits = details.movie_credits['cast'] 
    tv_credits = details.tv_credits['cast']

    cast = credits.cast
    crew = credits.crew
    cast_amt = len(cast)
    crew_amt = len(crew)

    bday = datetime.strptime(details.birthday, '%Y-%m-%d').date().strftime('%B %d, %Y')
    bday_date = datetime.strptime(details.birthday, '%Y-%m-%d').date()
    today = date.today()

    one_or_zero = ((today.month, today.day) < (bday_date.month, bday_date.day))
    year_difference = today.year - bday_date.year
    age = year_difference - one_or_zero

    knownfor = sorted(cast, key=lambda i:(i['vote_count'],i['vote_average'],i['popularity']), reverse=True)[:8]

    mov_cred = []
    tv_cred = []

    try:
        mc_filtered = list(filter(lambda x: (x['release_date'] != ''), movie_credits))
        mc = sorted(mc_filtered, key = lambda x: x.release_date[:4], reverse=True)
        mov_cred.append(mc)
    except Exception as e:
        pass

    try:
        tv_filtered = list(filter(lambda x: (x['first_air_date'] != ''), tv_credits))
        tv = sorted(tv_filtered, key = lambda x: x.first_air_date[:4], reverse=True)
        tv_cred.append(tv)
    except Exception as e:
        pass


    context = {
        'details':details,
        'credits':credits,
        'cast':cast,
        'crew':crew,
        'bday':bday,
        'age':age,
        'castamt':cast_amt,
        'crewamt':crew_amt,
        'knownfor':knownfor,
        'mov_cred':mov_cred,
        'tv_cred':tv_cred,
    }

    return render(
        request,
        'credits/creditsdetails.html',
        context,
    )




