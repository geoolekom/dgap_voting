from django.apps import AppConfig


class DepartmentsConfig(AppConfig):
    name = 'departments'
    verbose_name = 'Отделы'

    def ready(self):
        import departments.signals
