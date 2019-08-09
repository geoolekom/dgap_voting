from django.apps import AppConfig


class MaterialsConfig(AppConfig):
    name = 'materials'
    verbose_name = 'Материалы'

    def ready(self):
        import materials.signals
