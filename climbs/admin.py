# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from import_export import resources
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    pass
@admin.register(Gym)
class GymAdmin(ImportExportModelAdmin):
    model = Gym
    list_display =['name']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(Climb)
class ClimbAdmin(ImportExportModelAdmin):
    model = Climb
    list_display = ['anchor', 'status', 'date_created', 'date_retired', 'color',
        'grade', 'area', 'setter']
    list_filter = ['area__gym__name', 'status__status', 'date_created', 'setter__tag', 'grade__grade']
    search_fields = ['setter__tag', ]

@admin.register(Setter)
class SetterAdmin(ImportExportModelAdmin):
    pass

@admin.register(Color)
class ColorAdmin(ImportExportModelAdmin):
    pass

@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin):
    pass

@admin.register(Area)
class SetterAdmin(ImportExportModelAdmin):
    pass

@admin.register(Anchor)
class ClimbRouteAdmin(ImportExportModelAdmin):
    pass

@admin.register(Distribution)
class DistributionAdmin(ImportExportModelAdmin):
    pass

@admin.register(LocalDistribution)
class LocalDistributionAdmin(ImportExportModelAdmin):
    pass



# admin.site.register(Boulder)
# admin.site.register(Route)
# admin.site.register(Setter)
# admin.site.register(Gym)
# admin.site.register(Color)
# admin.site.register(Grade)
# admin.site.register(Area)
# admin.site.register(Climb)
# admin.site.register(ClimbRoute)
admin.site.register(Status)
# admin.site.register(Spread)
