from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from .models import Poll


@receiver(user_logged_in, dispatch_uid='polls')
def remind_to_vote(sender, request, **kwargs):
    user = request.user
    if user.is_authenticated:
        polls = [poll for poll in Poll.objects.filter(begin_date__lte=timezone.now(),
                                                      end_date__gte=timezone.now()).order_by('-begin_date') if
                 poll.is_user_target(user) and not poll.is_user_voted(user)]

        for poll in polls:
            messages.add_message(request, messages.INFO, 'Вам доступно голосование: <a class="alert-link" href="{}">{}</a>'
                                 .format(reverse("polls:available"), poll.name))
