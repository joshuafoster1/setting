# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Count, Min, Max
from django.db import models
import random
# Create your models here.
DATE = date.today()
class Gym(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    def get_total_climbs(self, climb_type):
        return Climb.objects.filter(area__gym=self, grade__climb=climb_type).count()

    def get_global_target_distribution(self, climb_type):
        global_dist = list(Distribution.objects.values('grade__grade', 'percent').filter(gym=self, grade__climb=climb_type))
        local_dict={}
        for item in global_dist:
            local_dict[item['grade__grade']]=item['percent']
        return local_dict

    def get_grade_count(self, climb_type):
        """{'vgrade':count}"""
        count = list(Climb.objects.values('grade__grade').filter(area__gym=self, grade__climb=climb_type, status__status='current').annotate(count = Count('grade')))
        local_dict={}
        for item in count:
            local_dict[item['grade__grade']]=item['count']
        return local_dict

    def create_climbs_to_set(self, request, areas, climb_type):
        def dict_max(dict):
            """
            return the key for the max value in dict. If there are multiple elements
            of the max value, it returns one at random.
            """
            v = list(dict.values())
            k = list(dict.keys())
            indices = [i for i, x in enumerate(v) if x == max(v)]
            randomEle = k[random.choice(indices)]
            return randomEle #k[v.index(max(v))]

        count = self.get_grade_count(climb_type)
        target_percent = self.get_global_target_distribution(climb_type)
        for area in areas:
            area_obj = Area.objects.get(location_name=area['area__location_name'], gym=self)
            climb_addition = int(request.POST.get(area['area__location_name']))

            grades_to_set=[]
            for _ in range(climb_addition):
                virtual_percent = area_obj.get_virtual_distribution(climb_type, count, climb_addition)
            # print(virtual_percent['V6'])
            # print(target_percent['V6'])

                perc_diff = {}
            # for grade_v, percent_v in virtual_percent.items():
            #     perc_diff[grade_v] = target_percent[grade_v] - percent_v
                for grade_t, percent_t in target_percent.items():
                    for grade_v, percent_v in virtual_percent.items():
                        if grade_v == grade_t:
                            diff = percent_t-percent_v
                            perc_diff[grade_t] = diff
                        else:
                            continue
                max_diff = dict_max(perc_diff)
                count[max_diff]+=1
                grades_to_set.append(max_diff)

            Climb.objects.bulk_create([Climb(date_created=DATE, color=Color.objects.get(pk=1), grade=Grade.objects.get(grade=grade), status=Status.objects.get(id=4), setter=Setter.objects.get(id=5), area=area_obj)for grade in grades_to_set])

        return grades_to_set


class Setter(models.Model):
    name = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_gym = models.ForeignKey(Gym)
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


class Distribution(models.Model):
    grade = models.ForeignKey(Grade, related_name='global_spread')
    percent = models.FloatField()
    gym = models.ForeignKey(Gym, related_name='global_spread')

    def __str__(self):
        return self.grade.grade + ' ' + str(self.percent)

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

    def get_total_climbs(self, climb_type):
        return Climb.objects.filter(area__gym=self.gym, grade__climb=climb_type).count()

    def get_grade_count(self, climb_type):
        """{'vgrade':count}"""
        count = list(Climb.objects.values('grade__grade').filter(area__gym=self.gym, grade__climb=climb_type, status__status='current').annotate(count = Count('grade')))
        local_dict={}
        for item in count:
            local_dict[item['grade__grade']]=item['count']
        return local_dict

    def get_global_target_distribution(self, climb_type):
        global_dist = list(Distribution.objects.values('grade__grade', 'percent').filter(gym=self.gym, grade__climb=climb_type))
        local_dict={}
        for item in global_dist:
            local_dict[item['grade__grade']]=item['percent']
        return local_dict

    def get_target_local_distribution(self):
        """{'vgrade':percent}"""
        spread= list(LocalDistribution.objects.values('grade__grade', 'percent').filter(area=self))
        local_dict={}
        for item in spread:
            local_dict[item['grade__grade']]=item['percent']
        return local_dict

    def get_virtual_distribution(self, climb_type, count, climb_addition=0):
        """
        current distribution for each grade by percentage (current%)
        """
        grade_count = count
        local_dict = {}
        for grade, count in grade_count.items():
            percentage = float(count)/(self.get_total_climbs(climb_type)+climb_addition)
            local_dict[grade]=percentage
        return local_dict

    def get_climbs_to_set(self, climb_addition, climb_type):
        def dict_max(dict):
            """
            return the key for the max value in dict. If there are multiple elements
            of the max value, it returns one at random.
            """
            v = list(dict.values())
            k = list(dict.keys())
            indices = [i for i, x in enumerate(v) if x == max(v)]
            randomEle = k[random.choice(indices)]
            return randomEle #k[v.index(max(v))]

        count = self.get_grade_count(climb_type)
        target_percent = self.get_global_target_distribution(climb_type)
        grades_to_set=[]
        for _ in range(climb_addition):
            virtual_percent = self.get_virtual_distribution(climb_type, count, climb_addition)
            # print(virtual_percent['V6'])
            # print(target_percent['V6'])

            perc_diff = {}
            # for grade_v, percent_v in virtual_percent.items():
            #     perc_diff[grade_v] = target_percent[grade_v] - percent_v
            for grade_t, percent_t in target_percent.items():
                for grade_v, percent_v in virtual_percent.items():
                    if grade_v == grade_t:
                        diff = percent_t-percent_v
                        perc_diff[grade_t] = diff
                    else:
                        continue
            max_diff = dict_max(perc_diff)
            print(max_diff, max(list(perc_diff.values())))
            count[max_diff]+=1
            print(count[max_diff])
            grades_to_set.append(max_diff)
        return grades_to_set


class LocalDistribution(models.Model):
    grade = models.ForeignKey(Grade, related_name='local_spread')
    percent = models.FloatField()
    area = models.ForeignKey(Area, related_name='local_spread')

    def __str__(self):
        return self.area.location_name + ' ' + str(self.percent)


class Anchor(models.Model):
    anchor = models.IntegerField()
    lead = models.BooleanField()
    toprope = models.BooleanField()

    def __str__(self):
        return str(self.anchor)


class Status(models.Model):
    CHOICES = (
        ('current', 'current'),
        ('retired', 'retired'),
        ('in progress', 'in progress'),
        ('in queue', 'in queue'),
    )
    status = models.CharField(choices=CHOICES, max_length=11)

    def __str__(self):
        return self.status

class Climb(models.Model):
    anchor = models.ForeignKey(Anchor, related_name = 'climbs',blank=True, null=True)
    status = models.ForeignKey(Status, related_name='climbs')
    date_created = models.DateField()
    date_retired = models.DateField(blank=True, null=True)
    color = models.ForeignKey(Color, related_name='climbs')
    grade = models.ForeignKey(Grade, related_name='climbs')
    area = models.ForeignKey(Area, related_name='climbs')
    setter = models.ForeignKey(Setter, related_name='climbs')

    def __str__(self):
        return self.color.color + ' ' + self.area.location_name
