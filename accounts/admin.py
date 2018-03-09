# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from training.models import Conditioning

# class ChoiceInline(admin.StackedInline):
#     model = Conditioning
#     extra = 3
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['category']}),
#         ('session', {'fields': ['exercise'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#
# admin.site.register(Conditioning, QuestionAdmin)
