# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from climbs.models import Anchor, Setter, Gym
# Create your models here.

class SafetyCheck(models.Model):
    gym = models.ForeignKey(Gym, related_name='safety_check')
    date = models.DateField()
    cpmpleted = models.BooleanField()

class AnchorsSafetyCheck(models.Model):
    safety_check = models.ForeignKey(SafetyCheck, related_name='safety_check_anchors')
    anchor = models.ForeignKey(Anchor, related_name='safety_check_anchors')
    comments = models.CharField(max_length=200)
    checked = models.BooleanField()


class Draw(models.Model):
    CHOICES = ((1,'Left'),
            (2, 'Right'),
            (0, 'Center'))
    anchor = models.ForeignKey(Anchor, related_name='draws')
    number = models.IntegerField()
    left_right_null = models.IntegerField(choices = CHOICES)
    bolt_replaced = models.BooleanField()
    hangar_tightened = models.BooleanField()
    hangar_replaced = models.BooleanField()
    quick_link_replaced = models.BooleanField()
    draw_replaced = models.BooleanField()
    carabiner = models.BooleanField()
    comment = models.CharField(max_length=150)
    setter = models.ForeignKey(Setter, related_name='safety_check_anchors')



Click on anchor, add draw check, select setter
