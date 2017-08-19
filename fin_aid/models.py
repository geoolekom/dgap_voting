from django.db import models
from django.contrib.auth.models import User

from hashlib import md5
from datetime import date


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    reason = models.CharField("Причина (для заявления)", max_length=100)
    max_sum = models.IntegerField("Макс. сумма", default=20000)
    max_quantity = models.IntegerField("Макс. раз за семестр", default=1)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


def get_next_payment_dttm(dt = None):
    pay_day = 28
    edge_day = 14
    if not dt:
        dt = date.today()
    year = dt.year
    if dt.day <= edge_day:
        month = dt.month
    else:
        if dt.month < 12:
            month = dt.month + 1
        else:
            month = 1
            year = dt.year + 1

    return date(year, month, pay_day)


class AidRequest(models.Model):
    WAITING = 1
    ACCEPTED = 2
    DECLINED = 3
    INFO_NEEDED = 4

    AID_REQUEST_STATUS = (
        (WAITING, "Заявление рассматривается"),
        (ACCEPTED, "Заявление одобрено"),
        (DECLINED, "В заявлении отказано"),
        (INFO_NEEDED, "Необходимо уточнить данные"),
    )

    applicant = models.ForeignKey(User, blank=True, null=True)  # find out how to add applicant to form before validation
    category = models.ForeignKey(Category)
    reason = models.TextField("Причина", max_length=1024)
    req_sum = models.FloatField("Запрошенная сумма", blank=True, null=True)
    urgent = models.BooleanField("Срочно", default=False)
    accepted_sum = models.FloatField("Одобренная сумма", blank=True, null=True)
    status = models.IntegerField("Статус заявления", choices=AID_REQUEST_STATUS, default=WAITING)
    add_dttm = models.DateTimeField("Дата подачи", auto_now_add=True)
    examination_dttm = models.DateTimeField("Дата рассмотрения", blank=True, null=True)
    payment_dttm = models.DateTimeField("Дата выплаты", blank=True, null=True)
    examination_comment = models.TextField("Комментарий комиссии", blank=True, null=True)
    submitted_paper = models.BooleanField("Принес заявление", default=False)

    def can_view(self, user):
        if not user.is_authenticated() or (self.applicant != user and not user.is_staff and not user.is_superuser):
            return False
        return True

    def __str__(self):
        return "{}: заявление от {} по категории {} на сумму {}".format(self.applicant, self.add_dttm.date(), self.category, self.req_sum)

    class Meta:
        verbose_name = "заявление на матпомощь"
        verbose_name_plural = "заявления на матпомощь"


# separate function as it's used in create_paper
def user_hash(user):
    secret = md5(str(user.id).encode("utf-8")).hexdigest()
    secret = md5((secret + user.username).encode("utf-8")).hexdigest()
    return secret


def document_path(instance, filename):
    return "aid_docs/user_{}/{}".format(user_hash(instance.request.applicant), filename)


# TODO if user can harm us with custom filename we should replace user-given filename
class AidDocument(models.Model):
    file = models.FileField("Документ", upload_to=document_path)
    # filename = models.CharField("Имя файла", max_length=100)
    request = models.ForeignKey(AidRequest)

    class Meta:
        verbose_name = "потверждающий документ"
        verbose_name_plural = "подтверждающие документы"

    def __str__(self):
        return "Документ {} к заявлению {}".format(self.file.name, self.request)
