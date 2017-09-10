from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AidRequestList.as_view(), name='index'),
    url(r'^request/(?P<pk>\d+)$', views.AidRequestDetail.as_view(), name='aid_request_detail'),
]