from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    reason = models.CharField("Причина (для заявления)", max_length=100)
    max_sum = models.IntegerField("Макс. сумма", default=20000)
    max_quantity = models.IntegerField("Макс. раз за семестр", default=1)

    def __str__(self):
        return self.name


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
        return "{}: заявление от {} по категории {} на сумму {}".format(self.applicant, self.add_dttm, self.category, self.req_sum)


def document_path(instance, filename):
    return "aid_docs/user_{}/{}".format(instance.request.applicant.id, filename)


class AidDocument(models.Model):
    file = models.FileField("Документ", upload_to=document_path)
    request = models.ForeignKey(AidRequest)

    def __str__(self):
        return "Документ {} к заявлению {}".format(self.file.name, self.request)
