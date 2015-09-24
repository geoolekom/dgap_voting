from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
    url(r'^$', views.profile_view, name='profile_view'),
    # url(r'^change_email/$', views.UserChangeEmail.as_view(), name='profile_change_email'),
    url(r'^change_subscribing/$', views.change_subscribing_status, name='change_subscribing'),
)
