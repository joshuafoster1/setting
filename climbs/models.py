# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from datetime import date

from django.db import models

# Create your models here.
DATE = date.today()


class Setter(models.Model):
    name = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_user_info(self):
        """User information in a list of tuples: Username, First Name, Last Name, email, Birthdate, Category"""

        user_info = []

        user_info.append(('User Name',self.user.username))
        user_info.append(('First Name', self.user.first_name))
        user_info.append(('Last Name', self.user.last_name))
        user_info.append(('Email', self.user.email))

        return user_info



class Grade(models.Model):
    CLIMBTYPE = (
        (1, 'Boulder'),
        (2, 'Route'),
    )

    grade = models.CharField(max_length=7)
    climb = models.IntegerField(choices=CLIMBTYPE)
    def __str__(self):
        return self.grade

class Gym(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Spread(models.Model):
    grade = models.ForeignKey(Grade, related_name='the_spread')
    quantity = models.IntegerField()
    gym = models.ForeignKey(Gym, related_name='the_spread')

class Color(models.Model):
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.color


class Area(models.Model):
    gym = models.ForeignKey(Gym, related_name='locations')
    location_name = models.CharField(max_length=30)
    number_of_climbs = models.IntegerField(blank=True)

    def __str__(self):
        return self.location_name

class Boulder(models.Model):
    date = models.DateField()
    color = models.ForeignKey(Color, related_name='boulders')
    grade = models.ForeignKey(Grade, related_name='boulders')
    area = models.ForeignKey(Area, related_name='boulders')
    setter = models.ForeignKey(Setter, related_name='boulders')

    def __str__(self):
        return str(self.color) + ' ' + str(self.grade)

class Route(models.Model):
    name = models.CharField(max_length=50, blank=True)
    date = models.DateField()
    color = models.ForeignKey(Color, related_name='routes')
    grade = models.ForeignKey(Grade, related_name='routes')
    area = models.ForeignKey(Area, related_name='routes')
    anchor = models.IntegerField()
    lead = models.BooleanField()
    toprope = models.BooleanField()
    setter = models.ForeignKey(Setter, related_name='routes')

    def __str__(self):
        return self.color + ' ' + self.area

class ClimbRoute(models.Model):
    anchor = models.IntegerField()
    lead = models.BooleanField()
    toprope = models.BooleanField()

    def __str__(self):
        return str(self.anchor)


class Status(models.Model):
    CHOICES = (
        ('current', 'current'),
        ('retired', 'retired'),
        ('in progress', 'in progress')
    )
    status = models.CharField(choices=CHOICES, max_length=11)

    def __str__(self):
        return self.status

class Climb(models.Model):
    climb_route = models.ForeignKey(ClimbRoute, related_name = 'climbs',blank=True, null=True)
    status = models.ForeignKey(Status, related_name='climbs')
    date_created = models.DateField()
    date_retired = models.DateField(blank=True, null=True)
    color = models.ForeignKey(Color, related_name='climbs')
    grade = models.ForeignKey(Grade, related_name='climbs')
    area = models.ForeignKey(Area, related_name='climbs')
    setter = models.ForeignKey(Setter, related_name='climbs')

    def __str__(self):
        return self.color.color + ' ' + self.area.location_name
