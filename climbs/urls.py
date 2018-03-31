from django.conf.urls import url, include
from django.contrib import admin

from climbs import views


urlpatterns = [
    url(r'^climbs/(?P<climb_type>[-\w]+)/$', views.climbs_list, name='climbs_list'),
    url(r'^new/$', views.climb_create, name = 'climb_create'),
    url(r'^delete/(?P<pk>\d+)/$', views.remove_climb, name = 'remove_climb'),
    url(r'^update/(?P<pk>\d+)/$', views.climb_update, name = 'climb_update'),
    url(r'^verify/$', views.climb_verification, name='climb_verification'),
    url(r'^climb/new_set/$', views.climb_set, name='climb_set'),
    url(r'^query/$', views.climb_query, name = 'climb_query'),
]
