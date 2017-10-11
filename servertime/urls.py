from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^servertime/$', TemplateView.as_view(template_name='servertime/servertime.html'), name='server_time'),
    url(r'^serverdate/$', TemplateView.as_view(template_name='servertime/serverdate.html'), name='server_date'),
    url(r'^servertimezone/$', TemplateView.as_view(template_name='servertime/servertimezone.html'), name='server_timezone'),
]
