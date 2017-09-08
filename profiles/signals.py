from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from django.contrib import messages
# from django.urls import reverse
from .models import UserProfile, StudentInfo


@receiver(post_save, sender=User, dispatch_uid='profiles')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
# move to views
#        url = reverse("blog:article_detail", kwargs={"slug": "notifications"})
#        messages.add_message(self.request, messages.INFO,
#                         "Регистрация прошла успешно. Осталось только <a href={}>настроить уведоления</a>".format(url))

# implemented through social_auth_pipeline (view settings.py)
"""@receiver(post_save, sender=UserSocialAuth, dispatch_uid="profiles")
def approve_user(sender, instance, created, **kwargs):
    if created:
        pass"""