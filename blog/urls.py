"""URL dispatcher for blog app

Used urls:
* Empty url redirects to news feed. See :class:`blog.views.ArticleList`
* post/<slug> and <slug> show detailed view of article (:class:`blog.views.ArticleDetail`). The first one is kept to keep
old urls valid
"""
from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.ArticleList.as_view(), name='index'),
    url(r'^$', views.ArticleList.as_view(), name='article_list'),
    url(r'^post/(?P<slug>[\w-]+)$', views.ArticleDetail.as_view(), name='article_detail_old'),
    url(r'^(?P<slug>[\w-]+)$', views.ArticleDetail.as_view(), name='article_detail'),
    #url(r'^new_post$', views.ArticleCreate.as_view(), name="new_post"),
]
