from django.dispatch import receiver
from django.db.models import signals

from accounts.models import User


@receiver(signals.post_save, sender=User)
def create_user_profile(instance, created=False):
    if created:
        from profiles.models import UserProfile
        UserProfile.objects.get_or_create(user=instance)
