from django.dispatch import receiver
from django.db.models import signals
from django.utils import timezone
from slugify import slugify

from materials.models import Category, Post, Article


@receiver(signals.pre_save, sender=Category)
def category_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(signals.pre_save, sender=Post)
def post_published_at(instance, *args, **kwargs):
    if instance.is_published and not instance.published_at:
        instance.published_at = timezone.now()


@receiver(signals.pre_save, sender=Article)
def article_published_at(instance, *args, **kwargs):
    if instance.is_published and not instance.published_at:
        instance.published_at = timezone.now()
