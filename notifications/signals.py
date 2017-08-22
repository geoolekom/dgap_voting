from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from fin_aid.models import AidRequest
from .notify import notify
from .templates import fin_aid_new_request, fin_aid_request_status_change


@receiver(post_save, sender=AidRequest, dispatch_uid='notifications')
def aidrequest_save(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(groups__name='finance')
        text = fin_aid_new_request(instance)
        for user in users:
            notify(user, text)
    else:
        if instance.status != AidRequest.WAITING:
            text = fin_aid_request_status_change(instance)
            notify(instance.applicant, text)
