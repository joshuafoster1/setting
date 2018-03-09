# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .tables import *
from django_tables2 import RequestConfig

# Create your views here.
def boulder_list(request, template_name='climbs/climbs_list.html'):
    if request.method =="POST":
        boulder_ids = Boulder.objects.filter(pk__in=list(request.POST.getlist('selection')))
        print(boulder_ids)

    boulders = Boulder.objects.filter(area__gym__name = 'Pipeworks')
    table = BoulderTable(boulders)
    RequestConfig(request).configure(table)
    return render(request, template_name, {'table': table})

def route_list(request, template_name='climbs/climbs_list.html'):
    if request.method =="POST":
        route_ids = Route.objects.filter(pk__in=list(request.POST.getlist('selection')))
        print(route_ids)

    routes = Route.objects.filter(area__gym__name = 'Pipeworks')
    table = RouteTable(routes)
    RequestConfig(request).configure(table)
    return render(request, template_name, {'table': table})


def boulder_create(request, template_name='climbs/boulder_form.html'):
    if request.method == 'POST':
        form = BoulderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boulder_list')
    else:
        form = BoulderForm()
    return render(request, template_name, {'form': form})

def formset(request, template_name='climbs/addmany_form.html'):
    if request.method == 'POST':
        form = AddmanyFormset()
    else:
        form=AddmanyFormset()
    return render(request, template_name, {'formset': form})
