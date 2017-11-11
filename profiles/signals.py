from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, StudentInfo


@receiver(post_save, sender=User, dispatch_uid='profiles')
def create_user_profile(sender, instance, created, **kwargs):
    """Receives ``post_save`` signal from :class:`User`. Creates :class:`profiles.models.Userprofile` for new users"""
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
# move to views
#        url = reverse("blog:article_detail", kwargs={"slug": "notifications"})
#        messages.add_message(self.request, messages.INFO,
#                         "Регистрация прошла успешно. Осталось только <a href={}>настроить уведоления</a>".format(url))


@receiver(post_save, sender=StudentInfo, dispatch_uid='profiles')
def update_student_info(sender, instance, created, **kwargs):
    """Receives ``post_save`` signal from :class:`profiles.models.StudentInfo`. Updates linked :class:`profiles.models.UserProfile`

    As :class:`UserProfile` is no longer used to store ersonal data, this function is unnecessary."""
    try:
        user = User.objects.get(username=instance.vk.split("/")[-1])
        if not user.userprofile.is_aproved:
            user.userprofile.is_approved = True
            user.userprofile.studentinfo = instance
            user.userprofile.group = instance.group
            user.userprofile.save()
            user.first_name = instance.first_name
            user.last_name = instance.last_name
            user.save()
    except Exception:
        pass

    try:
        user = User.objects.get(username=instance.phystech)
        if not user.userprofile.is_aproved:
            user.userprofile.is_approved = True
            user.userprofile.studentinfo = instance
            user.userprofile.group = instance.group
            user.userprofile.save()
            user.first_name = instance.first_name
            user.last_name = instance.last_name
            user.save()
    except Exception:
        pass


# implemented through social_auth_pipeline (view settings.py)
"""@receiver(post_save, sender=UserSocialAuth, dispatch_uid="profiles")
def approve_user(sender, instance, created, **kwargs):
    if created:
        pass"""

