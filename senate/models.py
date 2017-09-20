from django.db import models
from django.contrib.auth.models import User, Group


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    department = models.ForeignKey(Group, verbose_name="Отдел")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


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

    author = models.ForeignKey(User, verbose_name="Автор", null=True, blank=True)
    name = models.CharField("Имя", max_length=256)
    category = models.ForeignKey(Category, verbose_name="Категория")
    status = models.IntegerField("Статус", choices=STATUS, default=OPEN)
    add_dttm = models.DateTimeField("Дата создания", auto_now_add=True)
    last_event = models.DateTimeField("Последняя активность", default=None, blank=True, null=True)
    close_dttm = models.DateTimeField("Дата закрытия", blank=True, null=True, default=None)
    want_to_help = models.BooleanField("Хочу помогать", default=False)
    assigned_dept = models.ForeignKey(Group, verbose_name="Ответственный отдел", blank=True, null=True, default=None)
    assigned_worker = models.ForeignKey(User, verbose_name="Ответственный сотрудник", blank=True, null=True,
                                        default=None, related_name='assigned_worker')

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"

    def __str__(self):
        return "{}: {}".format(self.category, self.name)


class Event(models.Model):
    UPDATE = 1
    ASSIGNEE_CHANGE = 2
    STATUS_CHANGE = 3
    DETAILS_REQUEST = 4
    OPEN = 5

    CLASS = (
        (UPDATE, "Обновление"),
        (ASSIGNEE_CHANGE, "Смена ответственного"),
        (STATUS_CHANGE, "Изменение статуса"),
        (DETAILS_REQUEST, "Запрос сведений"),
        (OPEN, "Создание обращения")
    )

    MAX_INFO_LEN = 1024

    issue = models.ForeignKey(Issue, verbose_name="Обращение")
    author = models.ForeignKey(User, verbose_name="Автор", null=True, blank=True)
    add_dttm = models.DateTimeField("Дата создания", auto_now_add=True)
    cls = models.IntegerField("Класс", choices=CLASS, default=UPDATE)
    info = models.CharField("Информация", max_length=MAX_INFO_LEN, blank=True, null=True, default=None)
    new_dept = models.ForeignKey(Group, verbose_name="Новый отдел", blank=True, null=True, default=None)
    new_worker = models.ForeignKey(User, verbose_name="Новый сотрудник", blank=True, null=True,
                                   default=None, related_name='new_worker')
    new_status = models.IntegerField("Новый статус", choices=Issue.STATUS, default=Issue.CLOSED)

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"

    def __str__(self):
        return "{}: обновление от {}".format(self.issue, self.author)


class EventDocument(models.Model):
    file = models.ImageField("Изображение", upload_to='feedback/')
    event = models.ForeignKey(Event, verbose_name="Событие")
    # is_image = models.BooleanField("Является изображением", default=True)

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "документы"

    def __str__(self):
        return "Документ {} к событию {}".format(self.file.name, self.event)