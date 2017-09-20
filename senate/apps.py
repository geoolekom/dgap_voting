from django.apps import AppConfig


class SenateConfig(AppConfig):
    name = 'senate'
    verbose_name = "Сенат"
    import senate.signals
