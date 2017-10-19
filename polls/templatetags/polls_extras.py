from django.template import Library, Context

import logging

from polls.models import Poll


logger = logging.getLogger(__name__)
register = Library()


@register.inclusion_tag("polls/poll.html", takes_context=True)
def poll_panel(context, name):
    poll = Poll.objects.get(name=name)
    return {'poll': poll,}
