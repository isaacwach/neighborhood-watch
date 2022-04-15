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

@login_required(login_url='/accounts/login/')
@csrf_protect
def new_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile/profile.html', context)

def neighbourhoods(request):
    all_hoods = Neighbourhood.objects.all()
    all_hoods = all_hoods[::-1]
    context = {
        'all_hoods': all_hoods,
    }
    return render(request, 'neighbourhoods.html', context)

@login_required(login_url='/accounts/login/')
@csrf_protect
def create_neighbourhood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.admin = request.user
            neighbourhood.save()
            messages.success(
                request, 'You have succesfully created a Neighbourhood.Now proceed and join the Neighbourhood')
            return redirect('neighbourhood')
    else:
        form = NeighbourHoodForm()
    return render(request, 'new_hood.html', {'form': form})
    