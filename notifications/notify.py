from .models import UserNotificationsSettings, Notification
import vk
from dgap_voting.local_settings import VK_MESSAGES_TOKEN, DEBUG
from social.apps.django_app.default.models import UserSocialAuth

# import python-telegram-bot


vk_session = vk.Session(access_token=VK_MESSAGES_TOKEN)
vk_api = vk.API(vk_session)


def _get_vk_uid(user):
    social = UserSocialAuth.objects.get(user=user, provider="vk-oauth2")
    return social.uid


def _get_email(user):
    pass


def _get_telegram_uid(user):
    pass


def _notify_vk(user, text):
    response = vk_api.messages.send(user_id=_get_vk_uid(user), message=text)
    Notification.objects.create(user=user, method=Notification.VK, text=text, result=response)
    return response


def _notify_email(user, text):
    pass


def _notify_telegram(user, text):
    pass


def notify(user, text):
    if DEBUG:
        _notify_vk(user, text)
    else:
        settings = user.UserUserNotificationsSettings
        if settings.allow_vk:
            _notify_vk(user, text)
        if settings.allow_email:
            _notify_email(user, text)
        if settings.allow_telegram:
            _notify_telegram(user, text)
