"""Functions generating text for notifications."""

from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import dateformat
from django.contrib.sites.models import Site

from .notify import get_vk_uid, vk_message_user_link


def get_abs_url(loc_url):
    """Get absolute (including domain name) url based on ``loc_url`` provided.

    Should be moved to :mod:`core` app."""
    site = Site.objects.get_current().domain
    return "http://{}{}".format(site, loc_url)


def fin_aid_request_status_change(aid_request):
    """Message notifying student about examination of :class:`fin_aid.models.AidRequest`"""
    if aid_request.status == aid_request.ACCEPTED:
        s = "Одобрено заявление на матпомощь"
    elif aid_request.status == aid_request.DECLINED:
        s = "Отклонено заявление на матпомощь"
    elif aid_request.status == aid_request.INFO_NEEDED:
        url = get_abs_url(reverse("fin_aid:aid_request_update", args=[aid_request.pk]))
        s = "Необходимо уточнить информацию по заявлению на матпомощь. Редактировать заявление : {}".format(url)
    elif aid_request.status == aid_request.WAITING:
        s = "Ожидает рассмотрения заявление на матпомощь"
    else:
        raise ValueError("Неизвестный статус заявления на матпомощь")

    dt_add = dateformat.format(aid_request.add_dttm, settings.DATE_FORMAT)
    s += " от {} по категории '{}'\n".format(dt_add, aid_request.category)
    if aid_request.status == aid_request.ACCEPTED:
        dt_pay = dateformat.format(aid_request.payment_dt, settings.DATE_FORMAT)
        s += "Одобренная сумма: {}\n".format(aid_request.accepted_sum)
        if not aid_request.paid_with_cash:
            s += "Ожидаемая дата выплаты: {}\n".format( dt_pay)
        else:
            s += "Выплата наличными. Для уточнения деталей обращайтесь к [fizikaislove|стипкомиссии]"
    if aid_request.examination_comment:
        s += "Комментарий стип. комиссии: {}\n".format(aid_request.examination_comment)
    url = get_abs_url(reverse("fin_aid:aid_request_detail", args=[aid_request.pk]))
    if aid_request.status == aid_request.ACCEPTED and not aid_request.submitted_paper:
        s += "Не забудьте распечатать заявление из личного кабинета и опустить вместе с оригиналами документов в ящик пожеланий на 1 этаже общежития!\n"
    s += "Подробнее на сайте: {}".format(url)
    return s


def fin_aid_new_request(aid_request):
    """Message notifying treasurers about new aid requests"""
    s = "СРОЧНО: " if aid_request.urgent else ""
    s += "Новое заявление на матпомощь: {}\n".format(vk_message_user_link(aid_request.applicant),aid_request.applicant.first_name,
                                              aid_request.applicant.last_name, aid_request.category)
    s += "Обоснование: {}\nЗапрошенная сумма: {}".format(aid_request.reason, aid_request.req_sum)
    return s


# TODO return total sum of financial aid for the last month
def fin_aid_received(user):
    """Skeleton for message notifying student about aid received this month. SHould be send at time when scholarship is received"""
    pass


def poll_available(poll):
    """Message notifying user about available poll"""
    s = 'Ура, этот день настал! Вы можете принять участие в голосовании "{}". Оно пройдет с {} по {}.\n' \
        'Принять участие можно по ссылке: {}'
    url = get_abs_url(reverse("polls:available"))
    begin_date = dateformat.format(poll.begin_date, settings.DATETIME_FORMAT)
    end_date = dateformat.format(poll.end_date, settings.DATETIME_FORMAT)
    return s.format(poll.name, begin_date, end_date, url)


def bicycle_request_status_change(bicycle):
    """Message notifying user about examination of his bicycle storage request"""
    if bicycle.request_status == bicycle.ACCEPTED:
        s = "Одобрено заявление на место в велокомнате. Ваше место: {}".format(bicycle.place)
    elif bicycle.request_status == bicycle.DECLINED:
        s = "Отказано в заявлении на место в велокомнате"
    elif bicycle.request_status == bicycle.NO_PLACE:
        s = "Отказано в заявлении на велокомнату из-за отсутствия мест."
    elif bicycle.request_status == bicycle.WAITING:
        s = "Ожидает рассмотрения заявление на велокомнату"
    else:
        raise ValueError("Неизвестный статус заявления на место в велокомнате")
    return s


def bicycle_new_request(bicycle):
    """Message notifying staff about new cycle storage request"""
    s = "Новое заявление на велокомнату"
    return s