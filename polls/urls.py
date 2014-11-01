from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^servertime/$', views.server_time, name='server_time'),
    # ex: /polls/
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^closed/$', views.Closed.as_view(), name='closed'),
    url(r'^voted/$', views.Voted.as_view(), name='voted'),
    url(r'^available/$', views.Available.as_view(), name='available'),
    # ex: /polls/5/
    url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>\d+)/results/$', views.Results.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/results/detailed/$', views.detailed, name='detailed'),
    # ex:
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    # ex:
    url(r'^done/$', views.done, name='done'),
#    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile_view, name='profile_view'),
)
