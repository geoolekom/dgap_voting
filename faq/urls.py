from django.conf.urls import include, url
from faq import views

urlpatterns = [
    url(r'^$', views.Faq.as_view(), name='faq'),
]
