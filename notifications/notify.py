from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from .models import UserNotificationsSettings, Notification
import vk
from dgap_voting.local_settings import VK_MESSAGES_TOKEN, VK_GROUP_ID, DEBUG
from social_django.models import UserSocialAuth

# import python-telegram-bot


vk_session = vk.Session(access_token=VK_MESSAGES_TOKEN)
vk_api = vk.API(vk_session)


def get_vk_uid(user: User):
    try:
        social = UserSocialAuth.objects.get(user=user, provider="vk-oauth2")
        return social.uid
    except ObjectDoesNotExist:
        student_info = user.userprofile.student_info
        if not student_info:
            return None
        vk_userinfo = vk_api.users.get(user_ids=student_info.vk.split('/')[-1])
        return vk_userinfo[0]["uid"]


def get_email(user: User):
    pass


def get_telegram_uid(user: User):
    pass


def _notify_vk(user: User, text, title=None):
    response = vk_api.messages.send(user_id=get_vk_uid(user), message=text)
    Notification.objects.create(user=user, method=Notification.VK, text=text, result=response)
    return response


def _notify_email(user: User, text, title=None):
    pass


def _notify_telegram(user: User, text, title=None):
    pass


def vk_message_user_link(user):
    return "[id{}|{} {}]".format(get_vk_uid(user), user.first_name, user.last_name)


def vk_html_user_link(user):
    return '<a href="https://vk.com/{}" class="vk-link">{} {}</a>'.format(get_vk_uid(user), user.first_name, user.last_name)

def notify(user: User, text, title=None):
    try:
        settings = user.usernotificationssettings
        if settings.allow_vk:
            _notify_vk(user, text, title)
        if settings.allow_email:
            _notify_email(user, text, title)
        if settings.allow_telegram:
            _notify_telegram(user, text, title)
    except Exception:
        pass


def notify_group(group: Group, text, title=None):
    users = group.user_set.all()
    for user in users:
        notify(user, text, title)


# TODO if user has no VK? Currently returns True to avoid stupid messages
# TODO error handling?
def vk_messages_allowed(user):
    user_id = get_vk_uid(user)
    if user_id:
        try:
            request = vk_api.messages.isMessagesFromGroupAllowed(group_id=VK_GROUP_ID, user_id=user_id)
            if not request["is_allowed"]:
                return False
        except Exception:
            pass
    return True
