# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from .models import *
from datetime import date
DATE = date.today()

class TestRecommender(TestCase):
    grades = ['V1', 'V2', 'V3', 'V4', 'V5']
    areas = ['vert', 'steep', 'slab']

    def setup(self):
        Color.objects.create(color='Red')
        Red = Color.objects.get(color='Red')

        Grade.objects.bulk_create([Grade(grade=grade, climb= 1) for grade in grades])
        grade_db = Grade.objects.all()

        Gym.objects.create(name = 'the gym')
        the_gym = Gym.objects.get(name='the gym')

        Setter.objects.create()

        Area.objects.bulk_create([Area(gym = the_gym, location_name = area, number_of_climbs = 10) for area in areas])
        vert = Area.objects.get(name='vert')
        steep = Area.objects.get(name='steep')
        slab = Area.objects.get(name='slab')

        climb_vert = [Climb(status= 'current', date_created=DATE, color=Red, grade=grade, area=vert, setter=setter) for grade in grade_db]
        Climb.objects.bulk_create(climb_vert)

        climb_steep = [Climb(status= 'current', date_created=DATE, color=Red, grade=grade, area=steep, setter=setter) for grade in grade_db]
        Climb.objects.bulk_create(climb_steep)

        climb_slab = [Climb(status= 'current', date_created=DATE, color=Red, grade=grade, area=slab, setter=setter) for grade in grade_db]
        Climb.objects.bulk_create(climb_slab)
