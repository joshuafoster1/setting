# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from climbs.models import Setter
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import GymSelectionForm
import datetime
# Create your views here.


def get_user(request):
    pk = request.user.pk
    setter = get_object_or_404(Setter, user__pk=pk)
    return setter

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # NewSetter = Setter()
            # NewSetter.user = user
            # NewSetter.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    if request.method == 'POST':
        form = GymSelectionForm(request.POST)
        if form.is_valid():
            gym = form
            gym_name = gym.cleaned_data['name']
            request.session[gym_name] = gym_name
            request.session[gym_name].set_expriry(datetime.time(24,0,0,0))
            return redirect('home')
    else:
        form = GymSelectionForm()
    return render(request, 'home.html', {'form': form})

class UpdateSetter(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'accounts/update_setter.html'
    success_url = reverse_lazy('setter_info')

def setter_info(request):
    setter = get_user(request)
    info = setter.get_user_info()

    return render(request, 'accounts/setter_info.html', {'setter': setter, 'info': info})
