# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .tables import *
from django_tables2 import RequestConfig
from django.db.models import Count, Min, Max
import datetime

DATE = datetime.date.today()

# Create your views here.
def get_user(request):
    pk = request.user.pk
    setter = get_object_or_404(Setter, user__pk=pk)
    return setter

CLIMBTYPE = {'route': 2, 'boulder': 1}
GYM = 'Pipeworks'



def climb_query(request, climb_type='boulder'):
    gym = get_user(request).current_gym
    query = Climb.objects.values('date_created', 'area__location_name').filter(area__gym__name=gym).order_by('date_created').annotate(count = Count('grade'), min_grade=Min('grade__pk'), max_grade=Max('grade__pk'))
    table_data = []
    for item in list(query):
        print(item)
        grade_pk = []
        for item1 in list(query):
            if item['date_created'] == item1['date_created'] and item['area__location_name'] not in item1['area__location_name']:
                item['area__location_name'] += ' '+ item1['area__location_name']
                pk= [item['min_grade'],item['max_grade'], item1['min_grade'],item1['max_grade']]
                item['count'] += item1['count']
                grade_pk += pk
        if grade_pk:
            print(grade_pk)
            item['min_grade'] = Grade.objects.get(pk=min(grade_pk)).grade
            item['max_grade'] = Grade.objects.get(pk=max(grade_pk)).grade
        else:
            item['min_grade'] = Grade.objects.get(pk=item['min_grade']).grade
            item['max_grade'] = Grade.objects.get(pk=item['max_grade']).grade
        validater = []
        for route_set in table_data:
            validater.append(route_set['date_created'])
        if item['date_created'] not in validater:
            table_data.append(item)
    table = ClimbQuery(table_data)
    RequestConfig(request).configure(table)
    return render(request, 'climbs/climbs_list.html', {'table': table, 'gym': gym})

###TODO: create a table for the daily spread with a link in every row to update climbs
### can use list, then delete climbs from list and populate a table with climbs claimed
### for the day. once climbs are gone, leave a button to add climbs
###TODO: filter based on climb type to provide the correct grade type
def distribution(reset_num, climb_type= CLIMBTYPE['boulder'], gym = GYM):
    """
    returns list of tuples for the difference between desired climbs for grade and
    actual climbs per grade. Spread is gym scope not area scope.
    """
    print('start')
    test = Spread.objects.values('grade__grade', 'quantity').filter(gym__name=GYM, grade__climb=climb_type)
    climbs = Climb.objects.values('grade__grade').annotate(total=Count('grade')).filter(area__gym__name=GYM, grade__climb=climb_type, status__id = 1)
    print(test, 'split', climbs)
    grade_spread = []
    needed = 0
    for climb in climbs:
        climb_grade = climb['grade__grade']
        for desired in test:
            spread_grade = desired['grade__grade']
            print(spread_grade, climb_grade, 'here')
            if climb_grade == spread_grade:

                diff = int(desired['quantity']) - int(climb['total'])
                grade_spread.append((climb['grade__grade'], diff))
                needed = needed + diff
                print(diff, 'here')
    finalSpread = []
    for item in grade_spread:
        if item[1] > 0:
            per_grade = round(float(item[1])/float(needed) * float(reset_num))
            if per_grade >0:
                finalSpread.append([item[0], int(per_grade)])
    print(finalSpread)
    return finalSpread

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

        return render(request, 'climbs/replace_climbs.html', {'table': table, 'num_climbs': num_climbs, 'gym':gym, 'climb_type':climb_type })

    climbs = Climb.objects.filter(area__gym__name = gym).filter(grade__climb=CLIMBTYPE[climb_type], status__status='current')
    table = ClimbTable(climbs)
    RequestConfig(request).configure(table)
    print(distribution(2))
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
    #retire routes
    climb_ids = request.session['remove_climbs']
    Climb.objects.all().filter(pk__in=climb_ids).update(status=2, date_retired=DATE)
    if request.method == 'POST':
        set_num = request.POST.get('quantity', '')
        print(set_num)

        table_values = distribution(set_num)
        grade_spread = []
        for row in table_values:
            grade = [row[0]]
            grade_spread +=grade * row[1]
        table_list = []
        for grade in grade_spread:
            table_list.append({'grade': grade})
        print(table_list, set_num, climb_ids)
        table = GradeSpreadTable(table_list)
        RequestConfig(request).configure(table)

        return render(request, 'climbs/climb_set.html', {'table': table})

    # boulders = Boulder.objects.filter(pk__in=climb_ids)
