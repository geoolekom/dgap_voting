from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
import django.db.models.options as options
import re
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',) #добавление нового атрибута в мета

#TODO необходимые методы в моделях
#TODO метод approve_user и модели для базы поселения

class Poll(models.Model):
    name = models.CharField('Название опроса', max_length=200)
    question = models.CharField('Вопрос', max_length=200)
    begin_date = models.DateTimeField('Начало голосования')
    end_date = models.DateTimeField('Конец голосования')
    target_room = models.CharField('Целевая комната', max_length=200, default = r'^\d\d\d.?.?$') #предполагается использование регулярных выражений
    target_group = models.CharField('Целевая группа', max_length=200, default = r'^\d\d\d\d?.?$') 
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
    times_mailed = models.IntegerField(default=0) #how many times the mailing was made
    last_mailing = models.DateTimeField('Последняя рассылка', null=True) #when was the last informational mailing made
    
    def __str__(self):
        return self.name
    def is_closed(self):
        return self.end_date < timezone.now()
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
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User, null=True, blank=True, default = None)#при анонимном голосовании не заполнять это поле

class LegacyUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    dorm = models.IntegerField()
    room = models.CharField(max_length=10)
    card = models.CharField(unique=True, max_length=64)
    access_bicycle = models.IntegerField()
    birthday = models.DateField(blank=True, null=True)
    cardnumber = models.CharField(max_length=128)
    date = models.DateTimeField()
    expire = models.DateField(blank=True, null=True)
    enabled = models.IntegerField()
    access_laundry = models.IntegerField()
    address_confirmed = models.IntegerField()
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length=14)
    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'users'
        in_db = 'legacy_users'

class LegacyDorm(models.Model):
    id = models.IntegerField(primary_key=True)
    dorm = models.IntegerField()
    room = models.CharField(max_length=10)
    group = models.CharField(max_length=10)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    department = models.CharField(max_length=32)
    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)
    class Meta:
        managed = False
        db_table = 'dorm'
        in_db = 'legacy_users'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dorm = models.IntegerField(default=0)
    middlename = models.CharField('Отчество', max_length=100, blank=True)
    group = models.CharField('Номер группы', max_length=5, blank=True)
    room = models.CharField('Номер комнаты', max_length=4, blank=True)
    approval = models.BooleanField('Пользователь подтверждён', default=False)
    cardnumber = models.CharField('Последние пять цифр номера социальной карты', null=True, blank=True, max_length=5)
    is_subscribed = models.BooleanField('Пользователь подписан на рассылку', default=True)
    def __str__(self):  
        return "Профиль для %s" % self.user 
    def is_approved(self):
        return self.approval

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        profile, created = UserProfile.objects.get_or_create(user=instance) 

post_save.connect(create_user_profile, sender=User)
