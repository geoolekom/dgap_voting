from django.apps import AppConfig


class FinAidConfig(AppConfig):
    name = 'fin_aid'
    verbose_name = "Матпомощь"

    # def ready(self):
    #    import fin_aid.signals
