from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.ArticleList.as_view(), name='index'),
    url(r'^$', views.ArticleList.as_view(), name='article_list'),
    url(r'^(?P<slug>[\w-]+)$', views.ArticleDetail.as_view(), name='article_detail'),
    url(r'^post/(?P<slug>[\w-]+)$', views.ArticleDetail.as_view(), name='article_detail_old'),
    #url(r'^new_post$', views.ArticleCreate.as_view(), name="new_post"),
]
