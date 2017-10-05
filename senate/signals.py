from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import dateformat
from django.contrib.auth.models import Group
from datetime import datetime
import logging
from .models import Issue, Event, Employee
from notifications.notify import get_vk_uid, vk_message_user_link, notify, notify_group
from notifications.templates import get_abs_url
from core import settings

logger = logging.getLogger(__name__)


def new_issue_text(issue: Issue):
    author = vk_message_user_link(issue.author)
    s = "Новое обращение от {}\n{}\n".format(author, str(issue))
    event = issue.event_set.get(cls=Event.OPEN)
    if event.info:
        s += event.info + "\n"
    if issue.want_to_help:
        s += 'Студент готов помочь с реализацией\n'
    if issue.assigned_dept:
        s += "Ответственный отдел: {}\n".format(issue.assigned_dept.department.name)
    if issue.assigned_worker:
        s += "Ответственный сотрудник: {}\n".format(vk_message_user_link(issue.assigned_worker))
    s += "Подробнее на сайте: {}".format(get_abs_url(reverse("senate:issue_detail", args=[issue.pk])))
    return s


def issue_update_text(event: Event):
    issue = event.issue
    dt_add = dateformat.format(issue.add_dttm, settings.DATE_FORMAT)
    s = '{} обновил информация по обращению "{}" от {}\n'.format(vk_message_user_link(event.author), str(issue), dt_add)
    if event.new_status:
        s += "Новый статус: {}\n".format(event.get_new_status_display())
    if event.new_dept:
        s += "Обращение передано в {}\n".format(event.new_dept)
    if event.new_worker:
        s += "Теперь с обращением работает {}\n".format(vk_message_user_link(event.new_worker))
    if event.info:
        s += event.info + "\n"
    s += "Подробнее на сайте: {}".format(get_abs_url(reverse("senate:issue_detail", args=[issue.pk])))
    return s


@receiver(post_save, sender=Event, dispatch_uid='senate')
def event_save(sender, instance: Event, created, **kwargs):
    if created:
        issue = instance.issue
        issue.last_event = datetime.now()
        issue.save()
        if instance.cls == Event.OPEN:
            try:
                text = new_issue_text(issue)
            except Exception as e:
                text = "Новое обращение в отдел"
                logger.exception(e, exc_info=True, extra={'event': instance, 'created': created})
            notify_group(issue.assigned_dept, text)
        else:
            try:
                text = issue_update_text(instance)
            except Exception as e:
                text = "Информация по обращению в Сенат обновлена"
                logger.exception(e, exc_info=True, extra={'event': instance, 'created': created})
            if issue.author == instance.author:
                notify_group(issue.assigned_dept, text)
            else:
                notify(issue.author, text)

    if instance.new_status:
        instance.issue.status = instance.new_status
        instance.issue.save()
    if instance.new_dept:
        instance.issue.assigned_dept = instance.new_dept
        instance.issue.save()
    if instance.new_worker:
        instance.issue.assigned_worker = instance.new_worker
        instance.issue.save()


@receiver(post_save, sender=Employee, dispatch_uid='senate')
def employee_create(sender, instance: Employee, created, **kwargs):
        instance.person.groups.add(instance.department.group)
        instance.person.groups.add(Group.objects.get(name="senate_employee"))
        instance.person.save()
