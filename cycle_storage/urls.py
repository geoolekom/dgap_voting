from django.conf.urls import url
from cycle_storage import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^bicycle-(?P<pk>\d+)$', views.BicycleDetail.as_view(), name='bicycle_detail'),
    url(r'^add$', views.BicycleCreate.as_view(), name='bicycle_create'),
    url(r'^my$', views.MyBicycleDetail.as_view(), name='bicycle_my'),
]
