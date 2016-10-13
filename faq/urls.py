from django.conf.urls import patterns, include, url
from faq import views

urlpatterns = patterns('',
    url(r'^$', views.Faq.as_view(), name='faq'),
)