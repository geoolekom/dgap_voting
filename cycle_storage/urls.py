from django.conf.urls import url
from cycle_storage import views

urlpatterns = [
    url(r'^$', views.MyBicycleDetail.as_view(), name='index'),
    url(r'^view/(?P<pk>\d+)$', views.BicycleDetail.as_view(), name='bicycle_detail'),
    url(r'^delete/(?P<pk>\d+)$', views.BicycleDelete.as_view(), name='bicycle_delete'),
    url(r'^update/(?P<pk>\d+)$', views.BicycleUpdate.as_view(), name='bicycle_update'),
    url(r'^add$', views.BicycleCreate.as_view(), name='bicycle_create'),
    url(r'^my$', views.MyBicycleDetail.as_view(), name='bicycle_my'),
]
