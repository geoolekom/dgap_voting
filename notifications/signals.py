from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from fin_aid.models import AidRequest
from profiles.models import UserProfile
from .notify import notify
from .templates import fin_aid_new_request, fin_aid_request_status_change
from .models import UserNotificationsSettings


@receiver(post_save, sender=AidRequest, dispatch_uid='notifications')
def aidrequest_save_notify(sender, instance, created, **kwargs):
    # AirRequestCreate view form_valid() method creates aid request, ONLY THEN adds current user to it.
    # So when 'create' signal received, there is no aidrequest.applicant yet
    try:
        if not created:
            if instance.status == AidRequest.WAITING and instance.category.notifications:
                users = User.objects.filter(groups__name='finance')
                text = fin_aid_new_request(instance)
                for user in users:
                    notify(user, text)
            else:
                if instance.status != AidRequest.WAITING:
                    text = fin_aid_request_status_change(instance)
                    notify(instance.applicant, text)
    except Exception:
        pass


@receiver(post_save, sender=UserProfile, dispatch_uid='notifications')
def user_create(sender, instance, created, **kwargs):
    settings, created = UserNotificationsSettings.objects.get_or_create(user=instance.user)
    settings.allow_vk = instance.is_subscribed
    settings.save()


