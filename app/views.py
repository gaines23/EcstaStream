"""
Definition of views.
"""

from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.template import loader, Context
from django.http import HttpRequest
from .models import *
from .forms import *
from django.db.models import Count
from django.forms import ModelForm, inlineformset_factory
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.http import HttpResponse

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html'
    )

def TitlePage(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/TitlePage.html'
    )

