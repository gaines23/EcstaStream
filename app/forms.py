"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
import json
from datetime import date
from django.forms.widgets import *
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField



class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']



class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                                )
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'id']


class UpdateProfileForm(forms.ModelForm):
    profpic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    streaming_services = forms.ModelMultipleChoiceField(queryset=StreamingServices.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    fav_genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    

    class Meta:
        model = Profile
        fields = ['profpic', 'bio', 'id', 'streaming_services', 'fav_genres', ]


class FavoritePlaylistForm(forms.ModelForm):

    class Meta:
        model = FavoriteList
        fields = ['user', 'favorites', ]




#class FavoritePlaylist(forms.ModelForm):
#     share = forms.BooleanField()
#     private = forms.BooleanField()
     
#     class Meta:
#         model = FavoriteList
#         fields = ['id']