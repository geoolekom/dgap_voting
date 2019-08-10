from django.conf.urls import include, url, static
from django.conf import settings
from django.contrib import admin

admin.site.site_header = 'Сервисы ФОПФ'
admin.site.index_title = 'Администрирование сервисов ФОПФ'


urlpatterns = [
    # url(r'^$', ArticleList.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('materials.urls', namespace='materials')),
    url(r'^departments/', include('departments.urls', namespace='departments')),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^bicycle/', include('cycle_storage.urls', namespace='bicycle')),
    # url(r'^laundry/', RedirectView.as_view(url="http://stiralka.mipt.ru"), name="laundry"),
    # url(r'^print/', RedirectView.as_view(url="http://print.mipt.ru"), name="print"),
    url(r'^aid/', include('fin_aid.urls', namespace='fin_aid')),
    url(r'^senate/', include('senate.urls', namespace='senate')),
    url(r'^servertime/', include('servertime.urls', namespace='servertime')),
]
if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
