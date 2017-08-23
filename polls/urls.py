from django.conf.urls import url

from polls import views
from polls import admaking
from polls import mailing

urlpatterns = [
    # polls
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^closed/$', views.Closed.as_view(), name='closed'),
    url(r'^voted/$', views.Voted.as_view(), name='voted'),
    url(r'^available/$', views.Available.as_view(), name='available'),
    url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.Results.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/results/detailed/$', views.detailed, name='detailed'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<poll_id>\d+)/voters/$', views.voters, name='people'), 
    # done
    url(r'^done/$', views.done, name='done'),
    # ad making
    url(r'^(?P<poll_id>\d+)/pdf_advert/$', admaking.make_pdf, name='pdf_advert'),
    url(r'^(?P<poll_id>\d+)/create_advert/$', admaking.create_advert, name='create_advert'),
    # mailing
    url(r'^(?P<poll_id>\d+)/mail/$', mailing.mail_unvoted, name='mail'),
    url(r'^(?P<poll_id>\d+)/approve_mailing/$', mailing.approve_mailing, name='approve_mailing'),
]
