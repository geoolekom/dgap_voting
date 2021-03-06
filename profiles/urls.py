"""URL dispatcher for module :mod:`profiles`.

* At root url info about user is shown (see :func:`profiles.views.profile_view`)
* Call to ``change_subscribing`` url changes subscribing status - :func:`profiles.views.change_subscribing_status`
"""


from django.conf.urls import url

from profiles import views

urlpatterns = [
    url(r'^$', views.profile_view, name='profile_view'),
    # url(r'^change_email/$', views.UserChangeEmail.as_view(), name='profile_change_email'),
    url(r'^change_subscribing/$', views.change_subscribing_status, name='change_subscribing'),
]
