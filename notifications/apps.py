from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Configuration class for :mod:`notifications` module"""
    name = 'notifications'
    verbose_name = "Уведомления"

    def ready(self):
        """Connect :mod:`notifications.signals`"""
        import notifications.signals
