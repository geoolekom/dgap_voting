from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'
    verbose_name = "Уведомления"

    def ready(self):
        import notifications.signals
