from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """Configuration class for :mod:`profiles` module"""
    name = 'profiles'
    verbose_name = "Пользовательские профили"

    def ready(self):
        """Connect :mod:`profiles.signals`"""
        import profiles.signals
