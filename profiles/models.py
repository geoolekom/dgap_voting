from django.db import models
from django.contrib.auth.models import User
import django.db.models.options as options
from pandas import DataFrame
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',) # добавление нового атрибута в мета


# received from MIPT administration
class StudentInfo(models.Model):
    fio = models.CharField('ФИО', max_length=100, null=True, blank=True)
    group = models.CharField('Группа', max_length=10, null=True, blank=True)
    course = models.IntegerField(default=0)
    phystech = models.CharField('phystech.edu', max_length=50, null=True, blank=True)
    vk = models.CharField('vk', max_length=50, null=True, blank=True)
    first_name = models.CharField("Имя", max_length=100, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fio


def upload_students_list(filename='~/spiski.csv'):
    df = DataFrame.from_csv(filename, index_col=None)
    for i, row in df.iterrows():
        StudentInfo.objects.get_or_create(fio=row["ФИО"],
                                          group=row["Группа"],
                                          phystech=row["phystech"],
                                          vk=row["vk"],
                                          first_name=row["Имя"],
                                          last_name=row["Фамилия"])


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dorm = models.IntegerField(default=0)
    middlename = models.CharField('Отчество', max_length=100, blank=True)
    group = models.CharField('Номер группы', max_length=10, blank=True)
    room = models.CharField('Номер комнаты', max_length=4, blank=True)
    is_approved = models.BooleanField('Пользователь подтверждён', default=False)
    is_subscribed = models.BooleanField('Пользователь подписан на рассылку', default=True) # remove
    student_info = models.ForeignKey(StudentInfo, default=None, null=True, blank=True)

    def __str__(self):
        return "Профиль для %s" % self.user
