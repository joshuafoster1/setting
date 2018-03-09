from django.conf.urls import url, include
from django.contrib import admin

from climbs import views


urlpatterns = [
    url(r'^boulders$', views.boulder_list, name='boulder_list'),
    url(r'^routes$', views.route_list, name='route_list'),
    url(r'^new/$', views.boulder_create, name = 'boulder_new'),
    url(r'^manynew/$', views.formset, name='add_many'),
]
