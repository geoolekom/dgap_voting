from django.contrib import messages
from django.urls import reverse

from datetime import datetime

from notifications.notify import vk_messages_allowed


# TODO fails sometimes (eg when no app)
def resolver_context_processor(request):
    return {
        'app_name': request.resolver_match.app_name,
        'namespace': request.resolver_match.namespace,
        'url_name': request.resolver_match.url_name
    }

