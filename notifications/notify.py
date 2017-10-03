from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from social_django.models import UserSocialAuth
from hashlib import md5
import vk

from .models import UserNotificationsSettings, Notification
from dgap_voting.local_settings import VK_MESSAGES_TOKEN, VK_GROUP_ID, DEBUG


# import python-telegram-bot


vk_session = vk.Session(access_token=VK_MESSAGES_TOKEN)
vk_api = vk.API(vk_session, v='5.46')


def get_vk_uid(user: User):
    if user.is_authenticated:
        try:
            social = UserSocialAuth.objects.get(user=user, provider="vk-oauth2")
            return social.uid
        except ObjectDoesNotExist:
            student_info = user.userprofile.student_info
            if not student_info or not student_info.vk:
                return None
            vk_userinfo = vk_api.users.get(user_ids=student_info.vk.split('/')[-1])
            return vk_userinfo[0]["uid"]
    else:
        return None


def vk_message_user_link(user):
    if user.is_authenticated:
        vk_uid = get_vk_uid(user)
        if vk_uid:
            return "[id{}|{} {}]".format(vk_uid, user.first_name, user.last_name)
        else:
            return "{} {}".format(user.first_name, user.last_name)
    else:
        return "Анонимный пользователь"


def vk_html_user_link(user):
    if user.is_authenticated:
        vk_uid = get_vk_uid(user)
        if vk_uid:
            return '<a href="https://vk.com/{}" class="vk-link">{} {}</a>'.format(vk_uid, user.first_name, user.last_name)
        else:
            return "{} {}".format(user.first_name, user.last_name)
    else:
        return "Анонимный пользователь"


def get_email(user: User):
    pass


def get_telegram_uid(user: User):
    pass


def _notify_vk(user: User, text, title=None):
    hash = message_int_hash(user.username + text)
    response = vk_api.messages.send(user_id=get_vk_uid(user), message=text, random_id=hash)
    Notification.objects.create(user=user, method=Notification.VK, text=text, result=response)
    return response


def _notify_email(user: User, text, title=None):
    pass


def _notify_telegram(user: User, text, title=None):
    pass


def message_int_hash(text):
    hash = int(md5(text.encode("utf-8")).hexdigest(), 16)
    return abs(hash % 10**6)


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


def notify_group(group, text, title=None):
    if type(group) == str:
        group_object = Group.objects.get(name=group)
    else:
        group_object = group
    users = group_object.user_set.all()
    for user in users:
        try:
            notify(user, text, title)
        except Exception:
            pass


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
