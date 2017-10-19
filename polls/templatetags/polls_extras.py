from django.template import Library, Context

import logging

from polls.models import Poll


logger = logging.getLogger(__name__)
register = Library()


@register.inclusion_tag("polls/poll.html", takes_context=True)
def poll_panel(context, name):
    poll = Poll.objects.get(name=name)
    user = context["request"].user
    if poll.is_user_voted(user):
        target = 'voted'
    elif poll.is_user_target(user) and poll.is_started() and not poll.is_closed():
        target = 'available'
    else:
        target = 'not available'

    return {'poll': poll, "target": target}
