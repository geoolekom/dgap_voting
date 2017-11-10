"""Super obvious admin module"""

from django.contrib import admin
from .models import Notification, UserNotificationsSettings


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'send_dttm', 'method', 'text', 'result')


class UserNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'allow_vk', 'allow_email', 'allow_telegram')


admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserNotificationsSettings, UserNotificationSettingsAdmin)
