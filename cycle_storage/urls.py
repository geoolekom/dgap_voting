from django.conf.urls import url, static
from cycle_storage import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.MyBicycleDetail.as_view(), name='index'),
    url(r'^bicycle-(?P<pk>\d+)$', views.BicycleDetail.as_view(), name='bicycle_detail'),
]
