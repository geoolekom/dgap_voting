from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy

from files.models import Document
from profiles.models import StudentInfo


class Department(models.Model):
    group = models.OneToOneField(Group, verbose_name="Группа доступа", blank=True, null=True) # TODO if department needs several groups?
    name = models.CharField("Название", max_length=100, null=True, blank=True)
    head = models.ForeignKey(User, verbose_name="Глава отдела", null=True, blank=True)

    class Meta:
        verbose_name = "отдел Сената"
        verbose_name_plural = "отделы Сената"

    def __str__(self):
        return self.name

    def add_member(self, user):
        self.group.user_set.add(user)

    @property
    def members(self):
        return self.group.user_set.all()


class Employee(models.Model):
    person = models.ForeignKey(User)
    position = models.CharField("Должность", max_length=100)
    department = models.ForeignKey(Department, verbose_name="Отдел", blank=True, null=True, default=None)
    public = models.BooleanField("Публичный", default=True)
    phone = models.CharField("Телефон", max_length=100)
    importance = models.IntegerField("Значимость", default=1) # for sorting employee lists

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    department = models.ForeignKey(Group, verbose_name="Отдел")
    public = models.BooleanField("Показывать всем", default=True)

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
    category = models.ForeignKey(Category, verbose_name="Категория")
    name = models.CharField("Тема", max_length=256)
    status = models.IntegerField("Статус", choices=STATUS, default=OPEN)
    add_dttm = models.DateTimeField("Дата создания", auto_now_add=True)
    last_event = models.DateTimeField("Последняя активность", default=None, blank=True, null=True)
    close_dttm = models.DateTimeField("Дата закрытия", blank=True, null=True, default=None)
    want_to_help = models.BooleanField("Готов участвовать в реализации", default=False)
    assigned_dept = models.ForeignKey(Group, verbose_name="Ответственный отдел", blank=True, null=True, default=None)
    assigned_worker = models.ForeignKey(User, verbose_name="Ответственный сотрудник", blank=True, null=True,
                                        default=None, related_name='assigned_worker')

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"

    def __str__(self):
        return "{}: {}".format(self.category, self.name)

    def get_absolute_url(self):
        return reverse_lazy("senate:issue_detail", args=[self.id])


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

    MAX_INFO_LEN = 2048

    issue = models.ForeignKey(Issue, verbose_name="Обращение")
    author = models.ForeignKey(User, verbose_name="Автор", null=True, blank=True)
    add_dttm = models.DateTimeField("Дата создания", auto_now_add=True)
    cls = models.IntegerField("Класс", choices=CLASS, default=UPDATE)
    info = models.CharField("Информация", max_length=MAX_INFO_LEN, blank=True, null=True, default=None)
    new_dept = models.ForeignKey(Group, verbose_name="Новый отдел", blank=True, null=True, default=None)
    new_worker = models.ForeignKey(User, verbose_name="Новый сотрудник", blank=True, null=True,
                                   default=None, related_name='new_worker')
    new_status = models.IntegerField("Новый статус", choices=Issue.STATUS, null=True, blank=True, default=None)
    documents = GenericRelation(Document)

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"

    def __str__(self):
        return "{}: обновление от {}".format(self.issue, self.author)

    def images_tags(self):
        html = ""
        files = self.documents.all()
        for file in files:
            html += '<img class="aiddocument" style="max-width:100%;" src={}>'.format(file.file.url)
        return html
    images_tags.allow_tags = True
    images_tags.short_description = "Приложенные изображения"


