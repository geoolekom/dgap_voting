from django.db import models
from django.contrib.auth.models import User


class UserNotificationsSettings(models.Model):
    """Model for storing user's notifications preferences.

    Currently :func:`profiles.views.change_subscribing_status` changes :class:`profiles.models.UserProfile`,
    that triggers :func:`notifications.signals.user_create` signal, which updates ``UserNotificationsSettings``."""
    user = models.OneToOneField(User)
    "OneToOne link to :class:`django.contrib.auth.models.user` instance"
    allow_email = models.BooleanField("Разрешить уведомления на эл. почту", default=False)
    """Boolean field"""
    allow_vk = models.BooleanField("Разрешить уведомления Вконтакте", default=True)
    """Boolean field"""
    allow_telegram = models.BooleanField("Разрешить уведомления в Telegram", default=False)
    """Boolean field"""
    last_allow_vk_reminder = models.DateTimeField("Просили включить уведомления ВК", default=None, blank=True, null=True)
    """Date & time of last reminder (message on site) to allow vk messages. Used by :func:`notifications.signals.allow_vk_messages`
    
    Maybe such reminders should be stored in table like :class:`Notifications`?"""
    class Meta:
        verbose_name = "настройки уведомлений пользователя"
        verbose_name_plural = "настройки уведомлений пользователей"


class Notification(models.Model):
    "All sent notifications"
    MAIL = 1
    VK = 2
    TELEGRAM = 3
    METHODS = [
        (MAIL, "e-mail"),
        (VK, "Вконтакте"),
        (TELEGRAM, "telegram")
    ]
    """List of all available notifications providers."""
    user = models.OneToOneField(User)
    "OneToOne link to :class:`django.contrib.auth.models.User` instance"
    send_dttm = models.DateTimeField("Отправлено", auto_now_add=True)
    "Added automatically"
    method = models.IntegerField("Способ", choices=METHODS)
    """Notifications provider. Choices are stored in :const:`METHODS`"""
    text = models.TextField("Текст", max_length=1024)
    """Notification text. No escaping & so on is provided!"""
    result = models.CharField("Результат", max_length=256)
    """Provider's response to message sending attempt. VK returns message_id if success or error message when smth goes wrong"""

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"
