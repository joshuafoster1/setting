# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from import_export import resources
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(Gym)
class GymAdmin(ImportExportModelAdmin):
    pass

@admin.register(Climb)
class ClimbAdmin(ImportExportModelAdmin):
    pass

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

@admin.register(ClimbRoute)
class ClimbRouteAdmin(ImportExportModelAdmin):
    pass

@admin.register(Spread)
class SpreadAdmin(ImportExportModelAdmin):
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
