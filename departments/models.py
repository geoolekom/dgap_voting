from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

from departments.managers import VacancyQuerySet


class Department(models.Model):
    class Meta:
        verbose_name = 'отдел Сената'
        verbose_name_plural = 'отделы Сената'

    name = models.CharField(verbose_name='название', max_length=128)
    slug = models.SlugField(blank=True)
    description = RichTextField(verbose_name='описание', max_length=2048, blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = 'должности'

    name = models.CharField(verbose_name='название', max_length=128)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    class Meta:
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'

    position = models.ForeignKey('Position', verbose_name='должность', related_name='vacancies')
    department = models.ForeignKey('Department', verbose_name='отдел', related_name='vacancies')
    description = models.TextField(verbose_name='описание', max_length=2048, blank=True)

    is_open = models.BooleanField(verbose_name='открыта?', default=False)

    objects = VacancyQuerySet.as_manager()

    def __str__(self):
        return 'Вакансия "{0}" в {1}'.format(self.position, self.department)


# class VacancyResponse(models.Model):
#     class Meta:
#         verbose_name = 'отклик на вакансию'
#         verbose_name_plural = 'отклики на вакансию'
#
#     vacancy = models.ForeignKey('Vacancy', verbose_name='вакансия', related_name='responses')
#     text = models.TextField(verbose_name='текст отклика', max_length=1024)


class Activist(models.Model):
    class Meta:
        verbose_name = 'активист'
        verbose_name_plural = 'активисты'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь')
    department = models.ForeignKey('Department', verbose_name='отдел', related_name='activists')
    position = models.ForeignKey('Position', verbose_name='должность')

    description = models.TextField(verbose_name='описание', max_length=2048, blank=True)

    def __str__(self):
        return '{0} – {1} в {2}'.format(self.user.get_short_name(), self.position, self.department)
