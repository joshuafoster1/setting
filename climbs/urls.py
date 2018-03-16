from django.conf.urls import url, include
from django.contrib import admin

from climbs import views


urlpatterns = [
    url(r'^climbs/(?P<climb_type>[-\w]+)/$', views.climbs_list, name='climbs_list'),
    url(r'^routes$', views.route_list, name='route_list'),
    url(r'^new/$', views.boulder_create, name = 'boulder_new'),
    url(r'^manynew/$', views.formset, name='add_many'),
    url(r'^boulder/new_set/$', views.boulder_set, name='boulder_set'),
    url(r'^query/$', views.climb_query, name = 'climb_query'),
]
