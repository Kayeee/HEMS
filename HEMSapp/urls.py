from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from . import views, requests, apiViews

app_name = 'HEMSapp'
urlpatterns = [

    #views
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),


    #Request views
    url(r'^login$', requests.login, name='login'),
    url(r'^logout$', requests.logout, name='logout'),

    #API views
    url(r'^users/$', apiViews.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', apiViews.UserDetail.as_view()),
    url(r'^hemsboxes/$', apiViews.HemsBoxList.as_view()),
    url(r'^hemsboxes/(?P<pk>[0-9]+)/$', apiViews.HemsBoxDetail.as_view()),
    url(r'^solarpvs/$', apiViews.SolarPVList.as_view()),
    url(r'^solarpvs/(?P<pk>[0-9]+)/$', apiViews.SolarPVDetail.as_view()),
    url(r'^solarpvins/$', apiViews.SolarPVInList.as_view()),
    url(r'^solarpvins/(?P<pk>[a-zA-Z]+[0-9]+)/$', apiViews.SolarPVInDetail.as_view()),
    url(r'^solarpvouts/$', apiViews.SolarPVOutList.as_view()),
    url(r'^solarpvouts/(?P<pk>[a-zA-Z]+[0-9]+)/$', apiViews.SolarPVOutDetail.as_view()),
    url(r'^incidentradiations/$', apiViews.IncidentRadiationList.as_view()),
    url(r'^incidentradiations/(?P<pk>[0-9]+)/$', apiViews.IncidentRadiationDetail.as_view()),
    url(r'^dcpowers/$', apiViews.DCPowerList.as_view()),
    url(r'^dcpowers/(?P<pk>[0-9]+)/$', apiViews.DCPowerDetail.as_view()),
]
