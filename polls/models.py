from django.conf import settings
from django.db import models
from django.utils import timezone
import re

from profiles.models import StudentInfo, UserProfile


class Poll(models.Model):
    name = models.CharField('Название опроса', max_length=200)
    begin_date = models.DateTimeField('Начало голосования')
    end_date = models.DateTimeField('Конец голосования')
    target_room = models.CharField('Целевая комната', max_length=200, default=r'^')  # предполагается использование регулярных выражений
    target_group = models.CharField('Целевая группа', max_length=200, default=r'^')
    target_course = models.CharField('Курсы, которые голосуют', max_length=200, default=r'^')
    public = models.BooleanField('Открытое голосование', default=True)
    times_mailed = models.IntegerField(default=0, blank=True)  # how many times the mailing was made
    last_mailing = models.DateTimeField('Последняя рассылка', null=True)  # when was the last informational mailing made
    voted_users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    WITHOUT_TARGET_LIST = 'WITHOUT_TARGET_LIST'
    TARGET_LIST = 'TARGET_LIST'
    POLL_TYPE = (
        (WITHOUT_TARGET_LIST, 'WITHOUT TARGET LIST'),
        (TARGET_LIST, 'TARGET LIST'),
    )
    poll_type = models.CharField('Тип голосования', max_length=30, choices=POLL_TYPE,
                                 default=WITHOUT_TARGET_LIST)
    only_for_staff = models.BooleanField(default=False)
    # target_list = models.ManyToManyField(StudentInfo)
    # voted_users_from_list = models.ManyToManyField(StudentInfo)

    class Meta:
        verbose_name = "голосование"
        verbose_name_plural = "голосования"

    def __str__(self):
        return self.name

    def is_closed(self):
        return self.end_date < timezone.now()

    def is_started(self):
        return self.begin_date < timezone.now()

    def is_user_voted(self, user):
        if self.poll_type == Poll.TARGET_LIST:
            if not hasattr(user.userprofile.student_info, 'participant_set'):
                return True
            participants = user.userprofile.student_info.participant_set.all()
            if not participants:
                return True
            for item in participants:
                if item.poll.id == self.id:
                    return False if not item.voted else True
            return True
        else:
            return self.voted_users.filter(pk=user.pk).exists()

    def is_user_target(self, user):
        if self.poll_type == Poll.TARGET_LIST:
            if not hasattr(user.userprofile.student_info, 'participant_set'):
                return False
            participants = user.userprofile.student_info.participant_set.all()
            if not participants:
                return False
            for item in participants:
                if item.poll.id == self.id:
                    return True
            return False
        else:
            return ((re.compile(self.target_room, re.IGNORECASE)).match(user.userprofile.room) and
            (re.compile(self.target_group, re.IGNORECASE)).match(user.userprofile.group))

    def create_target_list_from_group_room_course(self, group=None, room=None, course=None,
                                                  only_staff=False):
        if self.poll_type != self.TARGET_LIST:
            return

        if only_staff:
            users = UserProfile.objects.filter(user__is_staff=True).all()
            for user in users:
                if user.student_info:
                    if not self.participant_set.filter(user_information=user.student_info):
                        Participant.objects.create(user_information=user.student_info,
                                                   poll=self, voted=False)
            self.only_for_staff = True
            self.save()
            return

        target_list = None
        for item in list(zip([group, room, course], ['group', 'room', 'course'])):
            if item[0] is not None:
                if target_list is None:
                    target_list = StudentInfo.objects.filter(
                        **{str(item[1])+'__iregex': item[0]}
                    ).all()
                else:
                    target_list = target_list.filter(
                        **{str(item[1])+'__iregex': item[0]}
                    )
        for user in target_list:
            Participant.objects.create(user_information=user, poll=self, voted=False)


class Question(models.Model):
    poll = models.ForeignKey(Poll)
    question = models.CharField('Вопрос', max_length=200)
    ONE = 'ONE'
    MANY = 'MANY'
    OWN = 'OWN'
    ANSWER_TYPE_CHOICES = (
        (ONE, 'Выбор одного варианта'),
        (MANY, 'Выбор нескольких вариантов'),
        (OWN, 'Свой вариант'),
    )
    answer_type = models.CharField('Тип ответа', max_length=10, choices=ANSWER_TYPE_CHOICES, default=ONE)
    CREATION = 'created'
    RANDOM = '?'
    ORDER_TYPES = (
        (CREATION, 'В порядке добавления'),
        (RANDOM, 'В случайном порядке'),
    )
    choices_order = models.CharField('Порядок вариантов ответа', max_length=10, choices=ORDER_TYPES, default=CREATION)
    required = models.BooleanField("Обязательный вопрос", default=True)

    def get_ordered_choices(self):
        if self.poll.is_closed():
            return self.choice_set.all().order_by('-votes')
        else:
            return self.choice_set.all().order_by(self.choices_order)

    def __str__(self):
        return self.question


class Participant(models.Model):
    user_information = models.ForeignKey(StudentInfo, verbose_name="Инфо о студенте", default=None, null=True, blank=True)
    poll = models.ForeignKey(Poll, verbose_name="Голосование", default=None, null=True, blank=True)
    voted = models.BooleanField("Проголосовал", default=False)

    class Meta:
        verbose_name = "участник голосования"
        verbose_name_plural = "участники голосования"

    def __str__(self):
        return "%s" % self.user_information.fio


class Choice(models.Model):
    question = models.ForeignKey(Question, default=None, null=True, blank=True)
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
    value = models.BigIntegerField()  # для очень старых опросов планируется удалять хэши, оставляя результаты в виде файла
    # надо переосмыслить предыдущий комментарий
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None)  # при анонимном голосовании не заполнять это поле
