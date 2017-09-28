from django.db import models
from django.contrib.auth.models import User
import django.db.models.options as options
from pandas import DataFrame
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',) # добавление нового атрибута в мета


# received from MIPT administration
class StudentInfo(models.Model):
    MALE = 1
    FEMALE = 2
    SEX = [
        (MALE, "male"),
        (FEMALE, "female"),
    ]
    fio = models.CharField('ФИО', max_length=100, null=True, blank=True)
    group = models.CharField('Группа', max_length=10, null=True, blank=True)
    course = models.IntegerField("Курс", default=0)
    phystech = models.CharField('phystech.edu', max_length=50, null=True, blank=True)
    vk = models.CharField('vk', max_length=50, null=True, blank=True)
    first_name = models.CharField("Имя", max_length=100, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=100, null=True, blank=True)
    sex = models.IntegerField("Пол", choices=SEX, default=MALE)

    def __str__(self):
        return self.fio

    @staticmethod
    def upload_csv(filename='~/spiski.csv'):
        df = DataFrame.from_csv(filename, index_col=None)
        for i, row in df.iterrows():
            try:
                studentinfo, created = StudentInfo.objects.get_or_create(fio=row["ФИО"],
                                                                         group=row["Группа"],
                                                                         first_name=row["Имя"],
                                                                         last_name=row["Фамилия"])
                if row["Email"]:
                    studentinfo.phystech = row["Email"]
                if not studentinfo.vk and row["screen_name"]:
                    studentinfo.vk = row["screen_name"]
                if row["Пол"] == "Мужской":
                    studentinfo.sex = StudentInfo.MALE
                else:
                    studentinfo.sex = StudentInfo.FEMALE
                studentinfo.course = int(row["Курс"])
                studentinfo.save()
            except Exception:
                print(row["ФИО"], row["Группа"])


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


# checks if student1 and student2 are the same student (students can have multiple accounts)
def is_same_student(student1, student2):
    if not (student1.is_authenticated and student2.is_authenticated):
        return False
    return student1 == student2 \
        or student1.userprofile.student_info and student2.userprofile.student_info == student1.userprofile.student_info


# checks if student1 is the same student as student2 or student1 is admin with appropriate access rights
def is_same_student_or_admin(student1, student2, group_name):
    return is_same_student(student1, student2) or student1.groups.filter(name=group_name).exists() or student1.is_superuser
