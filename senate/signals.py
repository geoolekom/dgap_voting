"""from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .models import Issue, Event"""


# TODO notify group about new Issues
#@receiver(post_save, sender=Issue, dispatch_uid='senate')
#def open_issue(sender, instance: Issue, created, **kwargs):
#    if created:
#        instance.assigned_dept = instance.category.department
#        instance.save()

"""@receiver(post_save, sender=Event, dispatch_uid='senate')
def new_event(sender, instance: Event, created, **kwargs):
    if created:
        instance.issue.last_event = datetime.now()
        instance.issue.save()"""
