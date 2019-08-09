from django.dispatch import receiver
from django.db.models import signals
from slugify import slugify

from departments.models import Department


@receiver(signals.pre_save, sender=Department)
def department_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
