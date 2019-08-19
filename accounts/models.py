from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from accounts.managers import UserManager


class AbstractStudentInfo(models.Model):
    class Meta:
        abstract = True

    last_name = models.CharField(verbose_name='фамилия', max_length=50)
    first_name = models.CharField(verbose_name='имя', max_length=50)
    patronymic = models.CharField(verbose_name='отчество', max_length=50, blank=True)

    group = models.CharField(verbose_name='группа', max_length=10, blank=True)
    course = models.PositiveIntegerField(verbose_name='курс', null=True, blank=True)
    room = models.CharField(verbose_name='комната', max_length=32, blank=True)

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    SEX_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )
    sex = models.CharField(verbose_name='пол', choices=SEX_CHOICES, max_length=10, blank=True)

    def get_full_name(self):
        parts = (self.last_name, self.first_name, self.patronymic)
        return ' '.join(part for part in parts if part)

    def get_short_name(self):
        parts = (self.first_name, self.patronymic)
        parts = ('{0}.'.format(part[0]) for part in parts if part)
        return '{0} {1}'.format(self.last_name, ' '.join(parts))

    get_full_name.short_description = 'ФИО'
    get_short_name.short_description = 'ФИО'


class User(AbstractStudentInfo, AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False, verbose_name='персонал?')
    is_active = models.BooleanField(default=False, verbose_name='активен?')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')

    is_verified = models.BooleanField(default=False, verbose_name='проверен?')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = tuple()

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()


class StudentInfo(AbstractStudentInfo):
    class Meta:
        verbose_name = 'данные студента'
        verbose_name_plural = 'данные студентов'

    user = models.OneToOneField('User', verbose_name='пользователь', blank=True, null=True, related_name='info')
    email = models.EmailField(unique=True, null=True)
    vk_url = models.URLField(verbose_name='ссылка на профиль ВК', blank=True)

    def __str__(self):
        return 'Данные {0}'.format(self.get_short_name())