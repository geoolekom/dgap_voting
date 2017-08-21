from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import dateformat
from django.contrib.sites.models import Site


def get_abs_url(loc_url):
    site = Site.objects.get_current().domain
    return "http://{}{}".format(site, loc_url)


def fin_aid_request_status_change(aid_request):
    dt_add = dateformat.format(aid_request.add_dttm, settings.DATE_FORMAT)
    dt_pay = dateformat.format(aid_request.payment_dt, settings.DATE_FORMAT)
    s = "Статус заявления на матпомощь от {} по категории '{}' изменен на '{}'\n".format(dt_add,
                                                                                         aid_request.category,
                                                                                         aid_request.get_status_display())
    if aid_request.status == aid_request.ACCEPTED:
        s += "Одобренная сумма: {}\nОжидаемая дата выплаты: {}\n".format(aid_request.accepted_sum, dt_pay)
    if aid_request.examination_comment:
        s += "Комментарий стип. комиссии: {}\n".format(aid_request.examination_comment)
    url = get_abs_url(reverse("fin_aid:aid_request_detail", args=[aid_request.pk]))
    s += "Подробности на сайте: {}".format(url)
    return s


# TODO notify treasurer when new requests are added
def fin_aid_new_request(aid_request):
    pass


# TODO return total sum of financial aid for the last month
def fin_aid_received(user):
    pass


def poll_available(poll):
    s = 'Ура, этот день настал! Вы можете принять участие в голосовании "{}". Оно пройдет с {} по {}.\n' \
        'Принять участие можно по ссылке: {}'
    url = get_abs_url(reverse("polls:available"))
    begin_date = dateformat.format(poll.begin_date, settings.DATETIME_FORMAT)
    end_date = dateformat.format(poll.end_date, settings.DATETIME_FORMAT)
    return s.format(poll.name, begin_date, end_date, url)
