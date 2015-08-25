from django.conf.urls import patterns, url

from servertime import views

urlpatterns = patterns('',
    url(r'^servertime/$', views.server_time, name='server_time'),
    url(r'^serverdate/$', views.server_date, name='server_date'),
    url(r'^servertimezone/$', views.server_timezone, name='server_timezone'),
)
