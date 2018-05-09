# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .tables import *
from django_tables2 import RequestConfig
from django.db.models import Count, Min, Max
import datetime


### Globals

DATE = datetime.date.today()
CLIMBTYPE = {'route': 2, 'boulder': 1}

def get_user(request):
    pk = request.user.pk
    setter = get_object_or_404(Setter, user__pk=pk)
    return setter
def is_foreman(setter):
    user = User.objects.get(username = setter.user.username)
    return user.groups.filter(name='Foreman').exists()


### Views

def climb_query(request, climb_type='boulder'):
    gym = get_user(request).current_gym
    try:
        climb_selection = request.session['select_climbs']
    except:
        climb_selection =[]

    if request.method == "POST" and request.session.get('round_two'):
        climb_ids = list(request.POST.getlist('selection'))
        request.session['remove_climbs'] = climb_ids
        num_climbs = len(climb_ids)
        climbs = Climb.objects.filter(pk__in=climb_ids)
        areas = Climb.objects.values('area__location_name').filter(pk__in=climb_ids).annotate(count=Count('grade'))
        table = ClimbRemoveTable(climbs)
        return render(request, 'climbs/replace_climbs.html', {'table': table, 'areas': areas, 'gym':gym, 'climb_type':climb_type })

    elif request.method =="POST":
        request.session['round_two'] = True
        date_created = list(request.POST.getlist('selection'))
        climb_selection = date_created
        climbs = Climb.objects.filter(date_created__in=date_created, status__status='current')
        areas = Climb.objects.values('area__location_name').filter(date_created__in=date_created).annotate(count=Count('grade'))
        table = ClimbQueryTable(climbs)
        area = Area.objects.get(location_name='Alcove')
        return render(request, 'climbs/climbs_list.html', {'table': table, 'areas': areas, 'gym':gym, 'climb_type':climb_type })

    #Present summary of climbs by date
    query = Climb.objects.values('date_created', 'area__location_name').filter(area__gym__name=gym, status__status='current').order_by('date_created').annotate(count = Count('grade'), min_grade=Min('grade__pk'), max_grade=Max('grade__pk'))

    table_data = []
    for item in list(query):
        grade_pk = []
        for item1 in list(query):
            if item['date_created'] == item1['date_created'] and item['area__location_name'] not in item1['area__location_name']:
                item['area__location_name'] += ', '+ item1['area__location_name']
                pk= [item['min_grade'],item['max_grade'], item1['min_grade'],item1['max_grade']]
                item['count'] += item1['count']
                grade_pk += pk
        if grade_pk:
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
    table = ClimbQuery(table_data) #table_data
    RequestConfig(request).configure(table)
    return render(request, 'climbs/climbs_list.html', {'table': table, 'gym': gym})


def climb_verification(request):
    """
    take a queryset from the days climbs and populate in a formset.
    upon verification update all climbs from 'in progress' to 'current'.
    """
    setter = get_user(request)
    gym = setter.current_gym

    if request.method == "POST":

        gym = get_user(request).current_gym
        queue = Climb.objects.all().filter(status=4, area__gym__name = gym).delete()
        in_progress = Climb.objects.all().filter(status=3, area__gym__name = gym)

        status = Status.objects.get(status='current')
        for climb in in_progress:
            climb.status = status
            climb.save()
        return redirect('home')


    in_progress = Climb.objects.all().filter(status=3, area__gym__name = gym)
    in_progress_table = InProgressTable(in_progress)
    RequestConfig(request).configure(in_progress_table)

    return render(request, 'climbs/verification.html', {'table': in_progress_table})

def climbs_list(request, climb_type, template_name='climbs/climbs_list.html'):
    gym = get_user(request).current_gym
    if request.method =="POST":
        climb_ids = list(request.POST.getlist('selection'))
        request.session['remove_climbs'] = climb_ids
        num_climbs = len(climb_ids)
        climbs = Climb.objects.filter(pk__in=climb_ids)
        areas = Climb.objects.values('area__location_name').filter(pk__in=climb_ids).annotate(count=Count('grade'))
        table = ClimbRemoveTable(climbs)
        area = Area.objects.get(location_name='Alcove')
        return render(request, 'climbs/replace_climbs.html', {'table': table, 'areas': areas, 'gym':gym, 'climb_type':climb_type })

    climbs = Climb.objects.filter(area__gym__name = gym).filter(grade__climb=CLIMBTYPE[climb_type], status__status='current').order_by('date_created')
    table = ClimbTable(climbs)
    RequestConfig(request).configure(table)
    return render(request, template_name, {'table': table, 'gym': gym})


def revert_climb(request, pk):
    climb = Climb.objects.filter(pk=pk).update(status=4)
    # climb.status = 4
    # climb.save()
    #
    return redirect('climb_set')


def climb_create(request, template_name='climbs/climb_form.html'):
    if request.method == 'POST':
        form = ClimbCreateForm(request.POST)
        if form.is_valid():
            climb = form.save(commit=False)
            climb.status = Status.objects.get(status='in queue')
            climb.save()
            return redirect('climb_set')
    else:
        form = ClimbCreateForm()
    return render(request, template_name, {'form': form})

def queue_modify(request, pk):
    climb = Climb.objects.get(pk=pk)

    if request.method == "POST":
        form = ClimbQueueModifyForm(request.POST)
        if form.is_valid():
            update = form
            # climb.color = update.cleaned_data['color']
            # if update.cleaned_data['anchor']:
            #     climb.anchor = update.cleaned_data['anchor']
            # # climb.status = Status.objects.get(pk=3)
            # climb.setter = update.cleaned_data['setter']
            # climb.date_created = update.cleaned_data['date_created']
            climb.grade = update.cleaned_data['grade']
            climb.area = update.cleaned_data['area']
            climb.save()
            return redirect('verify_spread')

    else:
        form = ClimbQueueModifyForm(instance = climb)
    return render(request, 'climbs/climb_form.html', {'form': form})

def climb_update(request, pk):
    climb = Climb.objects.get(pk=pk)

    if request.method == "POST":
        form = ForemanClimbUpdateForm(request.POST)
        if form.is_valid():
            update = form
            climb.color = update.cleaned_data['color']
            if update.cleaned_data['anchor']:
                climb.anchor = update.cleaned_data['anchor']
            # climb.status = Status.objects.get(pk=3)
            climb.setter = update.cleaned_data['setter']
            climb.date_created = update.cleaned_data['date_created']
            climb.grade = update.cleaned_data['grade']
            climb.area = update.cleaned_data['area']
            climb.save()
            return redirect('climb_set')

    else:
        form = ForemanClimbUpdateForm(instance = climb)
    return render(request, 'climbs/climb_form.html', {'form': form})


def climb_select(request, pk, template_name='climbs/climb_form.html'):
    climb = Climb.objects.get(pk=pk)
    setter = get_user(request)

    if request.method == 'POST'and is_foreman(setter):
        form = ForemanClimbSelectForm(request.POST)
        if form.is_valid():
            update = form
            climb.color = update.cleaned_data['color']
            if update.cleaned_data['anchor']:
                climb.anchor = update.cleaned_data['anchor']
            climb.status = Status.objects.get(pk=3)
            climb.setter = update.cleaned_data['setter']

            climb.save()
            return redirect('climb_set')


    elif request.method == "POST":
        form = ClimbSelectForm(request.POST)
        if form.is_valid():
            update = form
            climb.color = update.cleaned_data['color']
            if update.cleaned_data['anchor']:
                climb.anchor = update.cleaned_data['anchor']
            climb.status = Status.objects.get(pk=3)
            climb.setter = setter

            climb.save()
            return redirect('climb_set')


    else:
        if is_foreman(setter):
            form = ForemanClimbSelectForm(instance = climb)
        else:
            form = ClimbSelectForm(instance= climb)
    return render(request, template_name, {'form': form})


def verify_spread(request):
    setter = get_user(request)
    gym = setter.current_gym
    if request.method == 'POST':
        formset = QueueFormset(request.POST)
        if formset.is_valid():
            queue = formset.save()

            return redirect('climb_set')

    else:
        formset = QueueFormset(queryset =Climb.objects.all().filter(status=4, area__gym__name = gym).order_by('grade'))
        # queue = Climb.objects.all().filter(status=4, area__gym__name = gym).order_by('grade')
        # queue_table = ForemanQueueTable(queue)
        # RequestConfig(request).configure(queue_table)

    return render(request, 'climbs/modify_spread.html', { 'formset':formset})# 'table': queue_table,


def climb_set(request):
    setter = get_user(request)
    gym = setter.current_gym
    request.session['round_two'] = False
    try:
        climb_ids = request.session['remove_climbs']
    except:
        climb_ids =[]

    if request.method == 'POST' and len(climb_ids) > 0:
        # Retire Climbs
        Climb.objects.all().filter(pk__in=climb_ids).update(status=2, date_retired=DATE)

        # Retrieve areas for new climbs
        areas = Climb.objects.values('area__location_name').filter(pk__in=climb_ids).annotate(count=Count('grade'))
        climb_type = Climb.objects.get(id=climb_ids[0]).grade.climb
        request.session['remove_climbs'] = ''

        # create queue
        gym.create_climbs_to_set(request, areas, climb_type)

        # display queue
        queue = Climb.objects.all().filter(status=4, area__gym__name = gym).order_by('grade')
        queue_table = QueueTable(queue)
        RequestConfig(request).configure(queue_table)

        #display climbs inprogress
        in_progress = Climb.objects.all().filter(status=3, area__gym__name = gym)
        in_progress_table = ClimbTable(in_progress)
        RequestConfig(request).configure(in_progress_table)

        return render(request, 'climbs/climb_set.html', {'table_len':queue.count, 'table': queue_table, 'in_progress_table': in_progress_table, 'gym':gym})
    else:
        queue = Climb.objects.all().filter(status=4, area__gym__name = gym).order_by('grade')
        queue_table = QueueTable(queue)
        RequestConfig(request).configure(queue_table)

        in_progress = Climb.objects.all().filter(status=3, area__gym__name = gym)
        in_progress_table = InProgressTable(in_progress)
        RequestConfig(request).configure(in_progress_table)

        return render(request, 'climbs/climb_set.html', {'table_len':queue.count, 'table': queue_table, 'in_progress_table': in_progress_table, 'gym':gym})
