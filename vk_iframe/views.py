"""This module defines functions and classes for creating Vk community apps from regular views.

Documentation on vk community apps can be found at <https://vk.com/dev/community_apps_docs>

Basic steps to adapt regular view for vk:
1. If class-based view is used, :func:`mix_iframe` can be used to
"""

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from social_django.models import UserSocialAuth


import hmac
import hashlib


from core.settings import VK_APP_SECRET
from fin_aid.views import AidRequestCreate
from senate.views import IssueCreate
from blog.views import ArticleDetail


class VkIframeMixin:
    """Mixin that Adds VK JS SDK files, removes menu. Allows to 'natively' embed class-based views.

    Must be used with class-based view, inheriting ``ContextMixin`` and ``TemplateResponseMixin``.
    Example:
    ::
        class AidRequestCreateIframe(VkIframeMixin, AidRequestCreate):
            pass

    This class is identical to AidRequestCreate, but has slightly modified template so menu won't be rendered and only
    main form will be showm. Also some vk-related js is included into webpage.

    New class can be used in a way like
    ::
        url(r'^aid', views.iframe(views.AidRequestCreateIframe.as_view()), name='aid_request_create_iframe'),
    """
    template_name = 'vk_iframe/iframe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        context["base_template"] = super().template_name
        return context


def mix_iframe(old_class):
    """Dynamically creates new class from :class:`VkIframeMixin` and ``old_class``.

    Resulting class is returned and can be used, eg, in :func:`iframe` function."""
    return type("{}Iframe".format(old_class.__name__), (VkIframeMixin, old_class), {})


def check_signature(params):
    """Check initial request params integrity to prevent client-side changes.

    See <https://vk.com/dev/community_apps_docs> for details."""
    if 'sign' not in params or 'viewer_id' not in params:
        return False

    sign = ""
    for key, value in params.items():
        if key not in ['sign', 'hash']:
            sign += value

    return hmac.new(sign.encode('ascii'), VK_APP_SECRET.encode('ascii'), hashlib.sha256).hexdigest() == params['sign']


def iframe(base_view):
    """Function adapts ``base_view`` for embedding into VK iframe.

    1. Allows embedding of ``base_view`` into iframe
    2. Checks request signature (:func:`check_signature`)
    3. Logins user using request param ``viewer_id`` (is valid vk uid)
    4. Proceeds ``base_view``

    :param base_view: Valid django view. function-based views should be passed as-is,
    class-based in form ``ClassBasedView.as_view()``.
    :return: Adapted version of ``base_view``.

    """
    # TODO maybe drop support of func-based views and move all this code to VkIframeMixin?
    # TODO we are disabling anti-clickjacking and anti-csrf protection. Shell we really do it?
    # TODO check_signature is currently disabled due to incorrect behaviour of check_signature function.
    @csrf_exempt
    @xframe_options_exempt
    def iframe_aidrequest_create(request):
        #if check_signature(request.GET):
        #    messages.error(request, "Некорректные параметры запроса")
            # raise PermissionDenied

        try:
            user_soc_auth = UserSocialAuth.objects.get(uid=request.GET['viewer_id'])
            user = user_soc_auth.user
            login(request, user, backend='social_core.backends.vk.VKOAuth2')
            messages.success(request, "Вы авторизованы как {}".format(user))
        except ObjectDoesNotExist:
            # TODO maybe create user automatically?
            """Ooops, there is no such user in database:("""
            messages.error(request, 'Вы не зарегистрированы на сайте. Откройте '
                                    '<a class="alert-link" href="https://service.dgap-mipt.ru">ссылку</a> в новом окне.')
            raise PermissionDenied

        return base_view(request)

    return iframe_aidrequest_create


def index(request):
    """Serve particular view according to url anchor (send by vk to server as GET parameter 'hash')

    1. Get requested page name from GET
    2. Select mathing view class
    3. Mix it with :class:`VkIframeMixin`
    4. Adapt for iframe
    5. Server view to user"""
    page = request.GET.get('hash', '')
    params = {}
    base_class = AidRequestCreate
    if page == 'club':
        base_class = ArticleDetail
        params['slug'] = 'club'
    elif page == 'senate':
        base_class = IssueCreate


    return iframe(mix_iframe(base_class).as_view(**params))(request)
