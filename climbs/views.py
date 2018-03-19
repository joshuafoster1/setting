# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .tables import *
from django_tables2 import RequestConfig
from django.db.models import Count
# Create your views here.
def get_user(request):
    pk = request.user.pk
    setter = get_object_or_404(Setter, user__pk=pk)
    return setter


CLIMBTYPE = {'route': 2, 'boulder': 1}
GYM = 'Pipeworks'

###TODO: filter the queryset to the current_gym of the user.
###TODO: connect to link in base.html
def climb_query(request, climb_type='boulder'):
    gym = get_user(request).current_gym
    query = Climb.objects.values('date_created', 'area__location_name').filter(area__gym__name=gym).order_by('date_created').annotate(count = Count('grade'))
    table = ClimbQuery(query)
    RequestConfig(request).configure(table)
    return render(request, 'climbs/climbs_list.html', {'table': table, 'gym': gym})

###TODO: create a table for the daily spread with a link in every row to update climbs
### can use list, then delete climbs from list and populate a table with climbs claimed
### for the day. once climbs are gone, leave a button to add climbs
def distribution(climb_type):
    test = Spread.objects.values('grade__grade', 'quantity').filter(gym__name=GYM)
    climbs = Climb.objects.values('grade__grade').annotate(total=Count('grade')).filter(area__gym__name=GYM)
    grade_spread = []
    for climb in climbs:
        climb_grade = climb['grade__grade']
        for desired in test:
            spread_grade = desired['grade__grade']
            if climb_grade == spread_grade:

                diff = int(desired['quantity']) - int(climb['total'])
                grade_spread.append((climb['grade__grade'], diff))
    return grade_spread

def climb_verification(request):
    """
    take a queryset from the days climbs and populate in a formset.
    upon verification update all climbs from 'in progress' to 'current'.
    """
    pass

def climbs_list(request, climb_type, template_name='climbs/climbs_list.html'):
    gym = get_user(request).current_gym
    if request.method =="POST":
        climb_ids = list(request.POST.getlist('selection'))
        request.session['remove_climbs'] = climb_ids
        num_climbs = len(climb_ids)
        climbs = Climb.objects.filter(pk__in=climb_ids)
        table = ClimbRemoveTable(climbs)

        return render(request, 'climbs/replace_climbs.html', {'table': table, 'num_climbs': num_climbs, 'gym':gym })

    climbs = Climb.objects.filter(area__gym__name = gym).filter(grade__climb=CLIMBTYPE[climb_type])
    table = ClimbTable(climbs)
    RequestConfig(request).configure(table)
    print(distribution('boulder'))
    return render(request, template_name, {'table': table, 'gym': gym})


def boulder_create(request, template_name='climbs/boulder_form.html'):
    if request.method == 'POST':
        form = BoulderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('climbs_list', 'boulder')
    else:
        form = BoulderForm()
    return render(request, template_name, {'form': form})


def formset(request, template_name='climbs/addmany_form.html'):
    if request.method == 'POST':
        form = AddmanyFormset()
    else:
        form=AddmanyFormset()
    return render(request, template_name, {'formset': form})


def climb_set(request):
    climb_ids = request.session['remove_climbs']
    reset_num = len(climb_ids)
    spread = ['V1']

    if len(spread) <= 1:
        climb = Climb.objects.create(status = 'in progress', date_created=DATE)
        return render(request, 'climbs/boulder_set.html', {'climbs': 'climb'})
    else:
        climbs = []
        for i in range(reset_num):
            # climb = Boulder.object.create(grade = )
            # climbs.append(climb)
            continue
        return render(request, 'climbs/boulder_set.html', {})

    # boulders = Boulder.objects.filter(pk__in=climb_ids)
