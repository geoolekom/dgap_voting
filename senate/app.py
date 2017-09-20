from django.apps import AppConfig


class SenateConfig(AppConfig):
    name = 'senate'
    verbose_name = "Сенат"

    def ready(self):
        import senate.signals
