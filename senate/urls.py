from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IssueList.as_view(), name='index'),
    url(r'^issues$', views.IssueList.as_view(), name='issue_list'),
    url(r'^issue/(?P<pk>\d+)$', views.IssueDetail.as_view(), name='issue_detail'),
    url(r'^new_issue$', views.IssueCreate.as_view(), name='issue_create'),
]