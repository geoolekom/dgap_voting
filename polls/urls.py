from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout, password_change, password_change_done

from polls import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.Index.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>\d+)/results/$', views.Results.as_view(), name='results'),
    # ex:
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    # ex:
    url(r'^done/$', views.done, name='done'),
    url(r'^login/$', login, {'template_name': 'polls/login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'template_name': 'polls/logout.html'}, name = 'logout'),
    url(r'^password_change/$', password_change, {'post_change_redirect': 'polls:password_change_done','template_name': 'polls/password_change.html'}, name = 'password_change'),
    url(r'^password_change_done/$', password_change_done, { 'template_name': 'polls/password_change_done.html'}, name = 'password_change_done'),
#    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile_view, name='profile_view'),
)
