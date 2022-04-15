from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import *
from .models import *
# Create your views here.

def index(request):
    return render(request,"index.html")

@login_required(login_url='/accounts/login/')
@csrf_protect
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')