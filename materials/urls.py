from django.conf.urls import url

from materials.views import Index, CategoryDetail, PostList, PostDetail, ArticleDetail

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),

    url(r'^categories/(?P<slug>[\-\w]+)/$', CategoryDetail.as_view(), name='category_detail'),
    url(r'^articles/(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article_detail'),

    url(r'^posts/$', PostList.as_view(), name='post_list'),
    url(r'^posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='post_detail'),
]
