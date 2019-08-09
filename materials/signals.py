from django.dispatch import receiver
from django.db.models import signals
from slugify import slugify

from materials.models import Category


@receiver(signals.pre_save, sender=Category)
def category_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
