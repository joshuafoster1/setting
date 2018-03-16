from django.conf.urls import url, include
from django.contrib import admin

from climbs import views


urlpatterns = [
    url(r'^climbs/(?P<climb_type>[-\w]+)/$', views.climbs_list, name='climbs_list'),
    url(r'^new/$', views.boulder_create, name = 'boulder_new'),
    url(r'^manynew/$', views.formset, name='add_many'),
    url(r'^climb/new_set/$', views.climb_set, name='climb_set'),
    url(r'^query/$', views.climb_query, name = 'climb_query'),
]
