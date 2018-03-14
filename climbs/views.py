# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .tables import *
from django_tables2 import RequestConfig

# Create your views here.
def boulder_list(request, template_name='climbs/climbs_list.html'):
    if request.method =="POST":
        climb_ids = list(request.POST.getlist('selection'))
        request.session['remove_boulder'] = climb_ids
        num_climbs = len(climb_ids)
        boulders = Boulder.objects.filter(pk__in=climb_ids)
        table = BoulderRemoveTable(boulders)

        return render(request, 'climbs/replace_climbs.html', {'table': table, 'num_climbs': num_climbs })

    boulders = Boulder.objects.filter(area__gym__name = 'Pipeworks')
    table = BoulderTable(boulders)
    RequestConfig(request).configure(table)
    return render(request, template_name, {'table': table})


def route_list(request, template_name='climbs/climbs_list.html'):
    if request.method =="POST":
        route_ids = Route.objects.filter(pk__in=list(request.POST.getlist('selection')))
        return render(request, 'climbs/replace_climbs.html', {'climbs': route_ids})

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

def boulder_set(request):
    climb_ids = request.session['remove_boulder']
    reset_num = len(climb_ids)
    if reset_num <= 1:
        # climb = Boulder.object.create(grade = )
        return render(request, 'climbs/boulder_set.html', {'climbs': 'climb'})
    else:
        climbs = []
        for i in range(reset_num):
            # climb = Boulder.object.create(grade = )
            # climbs.append(climb)
            continue
        return render(request, 'climbs/boulder_set.html', {})

    # boulders = Boulder.objects.filter(pk__in=climb_ids)
