from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from .models import UserProfile, StudentInfo


@receiver(post_save, sender=User, dispatch_uid='profiles')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# implemented through social_auth_pipeline (view settings.py)
"""@receiver(post_save, sender=UserSocialAuth, dispatch_uid="profiles")
def approve_user(sender, instance, created, **kwargs):
    if created:
        pass"""