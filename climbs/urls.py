from django.conf.urls import url, include
from django.contrib import admin

from climbs import views


urlpatterns = [
    url(r'^climbs/(?P<climb_type>[-\w]+)/$', views.climbs_list, name='climbs_list'),
    url(r'^new/$', views.climb_create, name = 'climb_create'),
    url(r'^revert/(?P<pk>\d+)/$', views.revert_climb, name = 'revert_climb'),
    url(r'^select/(?P<pk>\d+)/$', views.climb_select, name = 'climb_select'),
    url(r'^update/(?P<pk>\d+)/$', views.climb_update, name = 'climb_update'),
    url(r'^verify/$', views.climb_verification, name='climb_verification'),
    url(r'^climb/new_set/$', views.climb_set, name='climb_set'),
    url(r'^query/$', views.climb_query, name = 'climb_query'),
    url(r'^verify/spread/$', views.modify_spread, name='verify_spread'),
    url(r'^modify/queue/(?P<pk>\d+)/$', views.queue_modify, name='queue_modify'),
    url(r'^datatables/(?P<climb_type>[-\w]+)/$', views.climb_data, name='climb_data'),

]
