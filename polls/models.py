from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_bleach.models import BleachField
import re

class Poll(models.Model):
    name = models.CharField('Название опроса', max_length=200)
    question = models.CharField('Вопрос', max_length=200)
    begin_date = models.DateTimeField('Начало голосования')
    end_date = models.DateTimeField('Конец голосования')
    target_room = models.CharField('Целевая комната', max_length=200, default = r'^') #предполагается использование регулярных выражений
    target_group = models.CharField('Целевая группа', max_length=200, default = r'^')
    public = models.BooleanField('Открытое голосование', default = True)
    ONE = 'ONE'
    MANY = 'MANY'
    OWN = 'OWN'
    ANSWER_TYPE_CHOICES = (
        (ONE , 'Выбор одного варианта'),
        (MANY , 'Выбор нескольких вариантов'),
        (OWN , 'Свой вариант'),
    )
    answer_type = models.CharField('Тип ответа', max_length=10, choices = ANSWER_TYPE_CHOICES, default = ONE)
    CREATION = 'created'
    RANDOM = '?'
    ORDER_TYPES = (
        (CREATION, 'В порядке добавления'),
        (RANDOM, 'В случайном порядке'),
    )
    choices_order = models.CharField('Порядок вариантов ответа', max_length=10, choices = ORDER_TYPES, default = CREATION)
    voted_users = models.ManyToManyField(User)
    times_mailed = models.IntegerField(default=0, blank=True) #how many times the mailing was made
    last_mailing = models.DateTimeField('Последняя рассылка', null=True) #when was the last informational mailing made

    def __str__(self):
        return self.name
    def is_closed(self):
        return self.end_date < timezone.now()
    def is_started(self):
        return self.begin_date < timezone.now()
    def is_user_voted(self, user):
        return self.voted_users.filter(pk=user.pk).exists()
    def is_user_target(self, user):
        return ((re.compile(self.target_room, re.IGNORECASE)).match(user.userprofile.room) and
            (re.compile(self.target_group, re.IGNORECASE)).match(user.userprofile.group))
    def get_ordered_choices(self):
        if self.is_closed():
            return self.choice_set.all().order_by('-votes')
        else:
            return self.choice_set.all().order_by(self.choices_order)

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField("Текст ответа", max_length=800)
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(editable=False, null=True)
    def __str__(self):
        return self.choice_text
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Choice, self).save(*args, **kwargs)

class UserHash(models.Model):
    value = models.BigIntegerField()#для очень старых опросов планируется удалять хэши, оставляя результаты в виде файла
#надо переосмыслить предыдущий комментарий
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User, null=True, blank=True, default = None)#при анонимном голосовании не заполнять это поле

class QA(models.Model):
    VOTING = 'VOTING'
    ORGANAZIER = 'ORGANAZIER'
    AUDIENCE_CHOICES = (
        (VOTING, 'Голосующему'),
        (ORGANAZIER, 'Организатору голосования'),
    )
    audience = models.CharField(max_length=30, choices=AUDIENCE_CHOICES,
                                default=VOTING)
    question = models.CharField(max_length=800)
    answer = BleachField(max_length=800)

    def __str__(self):
        for item in self.AUDIENCE_CHOICES:
            if item[0] == self.audience:
                return item[1] + ': ' + self.question

    class Meta:
        verbose_name = 'Question/Answer'
        verbose_name_plural = 'Faq'
