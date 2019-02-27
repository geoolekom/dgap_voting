from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'
    verbose_name = "Голосовалка"

    def ready(self):
        import polls.signals
