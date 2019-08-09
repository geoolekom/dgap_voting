from django.db import models


class MaterialQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_published=True)
