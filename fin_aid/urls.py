from django.conf.urls import url
from fin_aid import views

urlpatterns = [
    url(r'^$', views.AidRequestList.as_view(), name='index'),
    url(r'^request-(?P<pk>\d+)$', views.AidRequestDetail.as_view(), name='aid_request_detail'),
    url(r'^requests$', views.AidRequestList.as_view(), name='aid_request_list'),
    url(r'^add$', views.AidRequestCreate.as_view(), name='aid_request_create'),
]
