from django.db import models
from django.contrib.auth.models import User


class UserNotificationsSettings(models.Model):
    user = models.OneToOneField(User)
    allow_email = models.BooleanField("Разрешить уведомления на эл. почту", default=False)
    allow_vk = models.BooleanField("Разрешить уведомления Вконтакте", default=True)
    allow_telegram = models.BooleanField("Разрешить уведомления в Telegram", default=False)
    last_allow_vk_reminder = models.DateTimeField("Просили включить уведомления ВК", default=None, blank=True, null=True)

    class Meta:
        verbose_name = "настройки уведомлений пользователя"
        verbose_name_plural = "настройки уведомлений пользователей"


class Notification(models.Model):
    MAIL = 1
    VK = 2
    TELEGRAM = 3
    METHODS = [
        (MAIL, "e-mail"),
        (VK, "Вконтакте"),
        (TELEGRAM, "telegram")
    ]

    user = models.OneToOneField(User)
    send_dttm = models.DateTimeField("Отправлено", auto_now_add=True)
    method = models.IntegerField("Способ", choices=METHODS)
    text = models.TextField("Текст", max_length=1024)
    result = models.CharField("Результат", max_length=256)

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"
