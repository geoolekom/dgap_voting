from django.conf.urls import url

from materials.views import Index, CategoryDetail

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^articles/(?P<slug>[\-\w]+)/$', CategoryDetail.as_view(), name='category_detail'),
]
