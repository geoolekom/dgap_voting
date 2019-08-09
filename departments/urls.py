from django.conf.urls import url

from departments.views import DepartmentDetail, ActivistDetail

urlpatterns = [
    url(r'^(?P<slug>[\-\w]+)/$', DepartmentDetail.as_view(), name='department_detail'),
    url(r'^activists/(?P<pk>\d+)/$', ActivistDetail.as_view(), name='activist_detail'),
]
