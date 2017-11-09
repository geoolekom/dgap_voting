from django.db import models
from django.contrib.auth.models import User
import django.db.models.options as options
from pandas import DataFrame
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',) # добавление нового атрибута в мета # TODO legacy?


# received from MIPT administration
class StudentInfo(models.Model):
    """Model for storing info about students. Created from administration database. If user is verificated as
    enrolled student (by vk profile or corporate email), :class:`StudentInfo` is linked with :class:`UserProfile`. See :func:`profiles.psa.approve_student`.
    """

    fio = models.CharField('ФИО', max_length=100, null=True, blank=True)
    """Student's full name"""
    group = models.CharField('Группа', max_length=10, null=True, blank=True)
    """Academic group. If data is taken from settlement database (like in 2017), for students in gap year group number is outdated. 
    Must be taken into account when managing elections.
    """
    course = models.IntegerField("Курс", default=0)
    """Course. Valid for students in gap year"""
    phystech = models.CharField('phystech.edu', max_length=50, null=True, blank=True)
    """Student's corporate email - name.surname@phystech.edu. Used for student's verification"""
    vk = models.CharField('vk', max_length=50, null=True, blank=True)
    """Link to student's vk.com profile. It is quite challenging to obtain links for all students, but during last two
    elections electoral commission did it so we only have to collect accounts of freshmen yearly, which is much easier.
    
    **This field includes https://   prefix and contains screen name, not id**!
    
    **https://vk.com/smnnk**, not vk.com/smmnk or https://vk.com/id28749823.
    
    """
    first_name = models.CharField("Имя", max_length=100, null=True, blank=True)
    """Student's first name"""
    last_name = models.CharField("Фамилия", max_length=100, null=True, blank=True)
    """Student's last name"""
    MALE = 1
    FEMALE = 2
    SEX = [
        (MALE, "male"),
        (FEMALE, "female"),
    ]
    sex = models.IntegerField("Пол", choices=SEX, default=MALE)
    """Student's sex. Currently used to obtain genitive case of user's name when creating official papers.
    
    See :mod:`fin_aid.create_paper`"""
    room = models.CharField('Номер комнаты', max_length=32, blank=True)
    "Student's room. Currently unused, but who knows?"

    class Meta:
        ordering = ['fio']

    def __str__(self):
        return self.fio

    # TODO suspend students not in csv (kicked out students)
    @staticmethod
    def upload_csv(filename='~/spiski.csv'):
        """Populate database from csv with student's data. CSV can be obtained, for example, from settlement database.
        :param str filename: file name (including path) of csv file with student's data
        """
        df = DataFrame.from_csv(filename, index_col=None)
        for i, row in df.iterrows():
            try:
                studentinfo, created = StudentInfo.objects.get_or_create(fio=row["ФИО"])
                studentinfo.group = row["Группа"]
                studentinfo.first_name = row["Имя"]
                studentinfo.last_name = row["Фамилия"]
                studentinfo.course = int(row["Курс"])
                if row["Email"]:
                    studentinfo.phystech = row["Email"]
                if row["screen_name"]:
                    studentinfo.vk = "https://vk.com/" + row["screen_name"]
                if row["Пол"] == "Мужской":
                    studentinfo.sex = StudentInfo.MALE
                else:
                    studentinfo.sex = StudentInfo.FEMALE

                studentinfo.save()
            except StudentInfo.MultipleObjectsReturned:
                print(row["ФИО"], row["Группа"])
            except TypeError:
                pass


class UserProfile(models.Model):
    """Helper model, created after each new user registration.

    Formerly stored essential data about user, now only links to :class:`StudentInfo`"""
    user = models.OneToOneField(User)
    """Link to user"""
    dorm = models.IntegerField(default=0)
    """Super legacy, lol"""
    middlename = models.CharField('Отчество', max_length=100, blank=True)
    """Legacy"""
    group = models.CharField('Номер группы', max_length=10, blank=True)
    """Legacy"""
    room = models.CharField('Номер комнаты', max_length=4, blank=True)
    """Legacy"""
    is_approved = models.BooleanField('Пользователь подтверждён', default=False)
    """``True`` if user is approved ad DGAP student. Variable is set in :func:`profiles.psa.approve_student`"""
    is_subscribed = models.BooleanField('Пользователь подписан на рассылку', default=True) # remove
    """Legacy, now notifications are moved to standalone app :mod:`notifications`, so this setting should migrate to
    :class:`notification.models.UserNotificationsSettings, because different nitification services are available 
    (vk, email, telegram)`
    """
    student_info = models.ForeignKey(StudentInfo, default=None, null=True, blank=True)
    """Link to StudentInfo"""
    def __str__(self):
        return "Профиль для %s" % self.user


# checks if student1 and student2 are the same student (students can have multiple accounts)
def is_same_student(student1: User, student2: User):
    """Returns `True` if student1 and student2 are linked to the same :class:`StudentInfo` (= they belong to one person)"""
    if not (student1.is_authenticated and student2.is_authenticated):
        return False
    return student1 == student2 \
        or student1.userprofile.student_info and student2.userprofile.student_info == student1.userprofile.student_info


# checks if student1 is the same student as student2 or student1 is admin with appropriate access rights
def is_same_student_or_admin(student1: User, student2: User, group_name):
    """Checks if student1 is the same student as student2 or student1 is admin with appropriate access rights.

    Returns ``True`` if both ``student1`` and ``student2`` are linked to the same :class:`StudentInfo`
    or ``student1`` has specific group or ``student1`` is superuser.
    Can be useful when checkng access/update permissions: student may create object from one social account and
    then login from another."""
    return is_same_student(student1, student2) or student1.groups.filter(name=group_name).exists() or student1.is_superuser


def same_users_list(user: User):
    """Get list of all users, associated with given user's :class:`StudentInfo`.

    Logins through different OAuth providers create multiple :class:`User` objects for one student. This function allows
    us to get list of all :class:`User` objects, belonging to the same student. It must be taken into account when working with
    user-related objects.

    Let's imagine fragment of `dispatch` method in `UpdateView`

    Correct usage:
    ::
        if author not in same_users_list(user):
            raise PermissionDenied

    Incorrect usage:
    ::
        if author != user:
            raise PermissionDenied

    """
    if user.userprofile.student_info:
        users = [profile.user for profile in user.userprofile.student_info.userprofile_set.all()]
    else:
        users = [user]
    return users
