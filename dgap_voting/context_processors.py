from django.contrib import messages
from django.urls import reverse

from datetime import datetime

from notifications.notify import vk_messages_allowed
from polls.models import Poll


def resolver_context_processor(request):
    return {
        'app_name': request.resolver_match.app_name,
        'namespace': request.resolver_match.namespace,
        'url_name': request.resolver_match.url_name
    }


def remind_to_allow_messages(request):
    user = request.user
    try:
        settings = user.usernotificationssettings
        if user.userprofile.is_subscribed and not vk_messages_allowed(user) and not settings.last_allow_vk_reminder:
            messages.add_message(request, messages.INFO, '<a class="alert-link" href={}>Настроить получение уведомлений ВКонтакте</a> '
            'для оперативного информарования о рассмотрении заявлений на матпомощь, обращений в Сенат и т.д.'
                                 .format(reverse("blog:article_detail", args=["notifications"])))
        settings.last_allow_vk_reminder = datetime.now()
        settings.save()
    except Exception:
        pass
    return {}


def remind_to_vote(request):
    user = request.user
    if user.is_authenticated:
        polls = [poll for poll in Poll.objects.filter(begin_date__lte=datetime.now(),
                                                      end_date__gte=datetime.now()).order_by('-begin_date') if
                 poll.is_user_target(user) and not poll.is_user_voted(user)]

        for poll in polls:
            messages.add_message(request, messages.INFO, 'Вам доступно голосование: <a class="alert-link" href="{}">{}</a>'
                                 .format(reverse("polls:available"), poll.name))
    return {}