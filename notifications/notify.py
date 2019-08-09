"""Functions for dealing with messages.

They take care of different notification providers, user's notifications settings, staff groups...

Currently only functions for vk.com are implemented, other are represented by skeletons

VK Api (v5.46) is actively used.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from accounts.models import User
from social_django.models import UserSocialAuth
from hashlib import md5
import vk

from notifications.models import Notification
from core.settings import VK_MESSAGES_TOKEN, VK_GROUP_ID


# import python-telegram-bot


vk_session = vk.Session(access_token=VK_MESSAGES_TOKEN)
vk_api = vk.API(vk_session, v='5.46')


def get_vk_uid(user: User):
    """Get user's **vk uid** or None

    If user logged not through vk, tries to find his vk profile in :class:`profiles.models.StudentInfo`
    UID needed (formerly?) for sendind messages, displaying beautiful links in VK messages and, maybe, some other staff

    Safe, as long as user is valid :class:`django.contrib.auth.models.User` instance, no additional checks are needed.
    """
    if user.is_authenticated:
        try:
            social = UserSocialAuth.objects.get(user=user, provider="vk-oauth2")
            return social.uid
        except ObjectDoesNotExist:
            student_info = user.userprofile.student_info
            if not student_info or not student_info.vk:
                return None
            vk_userinfo = vk_api.users.get(user_ids=student_info.vk.split('/')[-1])
            return vk_userinfo[0]["id"]
    else:
        return None


def vk_message_user_link(user):
    """Get code displaying **internal link** to user's profile for embedding into **vk messages**.

    If it's impossible to find user's vk, return user's name without a link.

    Safe, as long as user is valid :class:`django.contrib.auth.models.User` instance, no additional checks are needed.
    """
    if user.is_authenticated:
        vk_uid = get_vk_uid(user)
        if vk_uid:
            return "[id{}|{} {}]".format(vk_uid, user.first_name, user.last_name)
        else:
            return "{} {}".format(user.first_name, user.last_name)
    else:
        return "Анонимный пользователь"


def vk_html_user_link(user):
    """Get code displaying **html link** to user's profile.

    If it's impossible to find user's vk, return user's name without a link.

    Safe, as long as user is valid :class:`django.contrib.auth.models.User` instance, no additional checks are needed.
    """
    if user.is_authenticated:
        vk_uid = get_vk_uid(user)
        if vk_uid:
            return '<a href="https://vk.com/id{}" class="vk-link">{} {}</a>'.format(vk_uid, user.first_name, user.last_name)
        else:
            return "{} {}".format(user.first_name, user.last_name)
    else:
        return "Анонимный пользователь"


def get_email(user: User):
    """Skeleton for function, retrieving user's **email for notifications**"""
    pass


def get_telegram_uid(user: User):
    """Skeleton for function retrieving user's **telegram uid**"""
    pass


def _notify_vk(user: User, text, title=None):
    """Private finction, sends vk notifications"""
    uid = str(get_vk_uid(user))
    hash = message_int_hash(uid + text)
    response = vk_api.messages.send(user_id=get_vk_uid(user), message=text, random_id=hash)
    Notification.objects.create(user=user, method=Notification.VK, text=text, result=response)
    return response


def _notify_email(user: User, text, title=None):
    """Skeleton for internal function which sends email notifications"""
    pass


def _notify_telegram(user: User, text, title=None):
    """Skeleton for internal function which sends telegram notifications"""
    pass


def message_int_hash(text):
    """Generate hash by message text. Different mesasages get different hashes

    Used in vk api to prevent sending duplicate messages"""
    hash = int(md5(text.encode("utf-8")).hexdigest(), 16)
    return abs(hash % 10**6)


def notify(user: User, text, title=None):
    """Main function for sending notifications.

    Aggregates internal functions for managing different providers and,
    according to :class:`notifications.models.UserNotificationsSettings`, sends messages.

    "Safe and simple": no checks on user are required, just pass user and proper text.
    You don't have to worry if user has email of allowed messages from vk"""
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
    """Function for notifying whole department about some event.

    Based on :func:`notifications.notify.notify`.
    You only have to provide group (name or :class:`Group` instance) and message text."""
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
    """Returns ``True`` if user allowed vk notifications from our community or we can't find user's vk

    Useg, eg, to remind user allow messages:)"""
    user_id = get_vk_uid(user)
    if user_id:
        try:
            request = vk_api.messages.isMessagesFromGroupAllowed(group_id=VK_GROUP_ID, user_id=user_id)
            if not request["is_allowed"]:
                return False
        except Exception:
            pass
    return True
