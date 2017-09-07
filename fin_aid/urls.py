from django.conf.urls import url
from . import views
from blog.views import ArticleDetail

urlpatterns = [
    url(r'^$', views.AidRequestList.as_view(), name='index'),
    url(r'^request/(?P<pk>\d+)$', views.AidRequestDetail.as_view(), name='aid_request_detail'),
    url(r'^requests$', views.AidRequestList.as_view(), name='aid_request_list'),
    url(r'^add$', views.AidRequestCreate.as_view(), name='aid_request_create'),
    url(r'^delete/(?P<pk>\d+)$', views.AidRequestDelete.as_view(), name='aid_request_delete'),
    url(r'^update/(?P<pk>\d+)$', views.AidRequestUpdate.as_view(), name='aid_request_update'),
    url(r'^rules$', ArticleDetail.as_view(), {"slug": "fin_aid_rules"}, name='aid_request_rules', ),
]
