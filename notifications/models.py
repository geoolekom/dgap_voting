from django.db import models
from django.contrib.auth.models import User


class UserNotificationsSettings(models.Model):
    user = models.ForeignKey(User)
    allow_email = models.BooleanField("Разрешить уведомления на эл. почту", default=False)
    allow_vk = models.BooleanField("Разрешить уведомления Вконтакте", default=True)
    allow_telegram = models.BooleanField("Разрешить уведомления в Telegram", default=False)


class Notification(models.Model):
    MAIL = 1
    VK = 2
    TELEGRAM = 3
    METHODS = [
        (MAIL, "e-mail"),
        (VK, "Вконтакте"),
        (TELEGRAM, "telegram")
    ]

    user = models.ForeignKey(User)
    send_dttm = models.DateTimeField("Отправлено", auto_now_add=True)
    method = models.IntegerField("Способ", choices=METHODS)
    text = models.TextField("Текст", max_length=1024)
    result = models.CharField("Результат", max_length=256)
