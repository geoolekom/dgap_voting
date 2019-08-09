from django.db import models


class VacancyQuerySet(models.QuerySet):
    def open(self):
        return self.filter(is_open=True)
