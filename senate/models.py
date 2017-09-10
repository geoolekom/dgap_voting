from django.db import models
from django.contrib.auth.models import User, Group


class Category(models.Model):
    name = models.CharField("Название")
    department = models.ForeignKey(Group, verbose_name="Отдел")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Issue(models.Model):
    OPEN = 1
    CLOSED = 2
    ACCEPTED = 3
    DECLINED = 4
    STATUS = (
        (OPEN, "Открыто"),
        (CLOSED, "Закрыто"),
        (ACCEPTED, "Инициатива одобрена"),
        (DECLINED, "Инициатива отклонена")
    )

    name = models.CharField("Имя", max_length=256)
    category = models.ForeignKey(Category, verbose_name="Категория")
    status = models.IntegerField("Статус", choices=STATUS, default=OPEN)
    add_dttm = models.DateTimeField("Дата создания", auto_now_add=True)
    close_dttm = models.DateTimeField("Дата закрытия", blank=True, null=True, default=None)
    want_to_help = models.BooleanField("Хочу помогать", default=False)
    assigned_group = models.ForeignKey(Group, verbose_name="Ответственный отдел", blank=True, null=True, default=None)
    assigned_worker = models.ForeignKey(User, verbose_name="Ответственный сотрудник", blank=True, null=True, default=None)

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"


class Event(models.Model):
    UPDATE = 1
    ASSIGNEE_CHANGE = 2
    STATUS_CHANGE = 3
    DETAILS_REQUEST = 4
    START = 5

    CLASS = (
        (UPDATE, "Обновление"),
        (ASSIGNEE_CHANGE, "Смена ответственного"),
        (STATUS_CHANGE, "Изменение статуса"),
        (DETAILS_REQUEST, "Запрос сведений"),
        (START, "Создание обращения")
    )

    issue = models.ForeignKey(Issue, verbose_name="Обращение")
    cls = models.IntegerField("Класс", choices=CLASS, default=UPDATE)
    info = models.CharField("Информация", max_length=1024, blank=True, null=True, default=None)
    new_dept = models.ForeignKey(Group, verbose_name="Новый отдел", blank=True, null=True, default=None)
    new_worker = models.ForeignKey(User, verbose_name="Новый сотрудник", blank=True, null=True, default=None)

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"


class EventDocument(models.Model):
    file = models.FileField("Документ", upload_to=document_path)
    event = models.ForeignKey(Event, verbose_name="Событие")
    is_image = models.BooleanField("Является изображением", default=False)

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "документы"

    def __str__(self):
        return "Документ {} к заявлению {}".format(self.file.name, self.request)