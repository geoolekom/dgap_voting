from django.conf.urls import url
from blog.views import ArticleDetail
from . import views

urlpatterns = [
    url(r'^$', views.IssueList.as_view(), name='index'),
    url(r'^issues$', views.IssueList.as_view(), name='issue_list'),
    url(r'^issue/(?P<pk>\d+)$', views.IssueDetail.as_view(), name='issue_detail'),
    url(r'^new_issue$', views.IssueCreate.as_view(), name='issue_create'),
    url(r'^about$', ArticleDetail.as_view(), {"slug": "about_senate"}, name='about', ),
    url(r'^contacts$', ArticleDetail.as_view(), {"slug": "contacts"}, name='contacts', ),
]