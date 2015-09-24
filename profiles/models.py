from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',) #добавление нового атрибута в мета


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
    is_approved = models.BooleanField('Пользователь подтверждён', default = False)
    is_subscribed = models.BooleanField('Пользователь подписан на рассылку', default=True)

    def __str__(self):  
        return "Профиль для %s" % self.user 


def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        profile, created = UserProfile.objects.get_or_create(user=instance) 


post_save.connect(create_user_profile, sender=User)
