from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .models import Issue, Event


# TODO notify group about new Issues


@receiver(post_save, sender=Event, dispatch_uid='senate')
def event_save(sender, instance: Event, created, **kwargs):
    if created:
        instance.issue.last_event = datetime.now()
        instance.issue.save()
    if instance.new_status:
        instance.issue.status = instance.new_status
        instance.issue.save()
    if instance.new_dept:
        instance.issue.assigned_dept = instance.new_dept
        instance.issue.save()
    if instance.new_worker:
        instance.issue.assigned_worker = instance.new_worker
        instance.issue.save()

