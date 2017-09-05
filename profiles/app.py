from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    verbose_name = "Пользовательские профили"

    def ready(self):
        import profiles.signals
