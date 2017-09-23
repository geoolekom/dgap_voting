from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .models import Issue, Event
from notifications.notify import get_vk_uid, vk_message_user_link, notify, notify_group


def new_issue_text(issue: Issue):
    s = "Новое обращение от {}\n{}\n".format(vk_message_user_link(issue.author), str(issue))
    event = issue.event_set.get(cls=Event.OPEN)
    if event.info:
        s += event.info + "\n"
    if issue.want_to_help:
        s += 'Студент готов помочь с реализацией\n'
    if issue.assigned_dept:
        s += "Ответственный отдел: {}\n".format(issue.assigned_dept.department.name)
    if issue.assigned_worker:
        s += "Ответственный сотрудник: {}\n".format(vk_message_user_link(issue.assigned_worker))

    return s


def issue_update_text(event: Event):
    issue = event.issue
    s = '{} обновил информация по обращению "{}" от {:%d %B %Y}\n'.format(vk_message_user_link(event.author), str(issue), issue.add_dttm)
    if event.new_status:
        s += "Новый статус: {}\n".format(event.new_status)
    if event.new_dept:
        s += "Обращение передано в {}\n".format(event.new_dept)
    if event.new_worker:
        s += "Теперь с обращением работает {}\n".format(vk_message_user_link(event.new_worker))
    if event.info:
        s += event.info + "\n"

    return s


@receiver(post_save, sender=Event, dispatch_uid='senate')
def event_save(sender, instance: Event, created, **kwargs):
    if created:
        issue = instance.issue
        issue.last_event = datetime.now()
        issue.save()
        if instance.cls == Event.OPEN:
            notify_group(issue.assigned_dept, new_issue_text(issue))
        else:
            notify(issue.author, issue_update_text(instance))
    if instance.new_status:
        instance.issue.status = instance.new_status
        instance.issue.save()
    if instance.new_dept:
        instance.issue.assigned_dept = instance.new_dept
        instance.issue.save()
    if instance.new_worker:
        instance.issue.assigned_worker = instance.new_worker
        instance.issue.save()
