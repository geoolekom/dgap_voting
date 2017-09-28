from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from profiles.models import UserProfile


def bike_photo_path(instance, filename):
    return "bicycles/user{}_{}".format(instance.owner.id, filename)


class Bicycle(models.Model):
    WAITING = 1  # 'WAITING'
    ACCEPTED = 2  # 'ACCEPTED'
    DECLINED = 3  # 'DECLINED'
    NO_PLACE = 4  # 'NO_PLACE'
    BIKE_STATUS = (
        (WAITING, "Заявка рассматривается"),
        (ACCEPTED, "Одобрено"),
        (DECLINED, "Отказано"),
        (NO_PLACE, "Нет мест"),
    )

    owner = models.ForeignKey(User, blank=True, null=True, verbose_name="Владелец")
    manufacturer = models.CharField("Производитель", max_length=255, default="Неизвестно", blank=True, null=True)
    model = models.CharField("Модель", max_length=255, default="Неизвестно", blank=True, null=True)
    info = models.TextField("Доп. описание", max_length=1024, blank=True, null=True)
    add_dttm = models.DateTimeField('Publish datetime', auto_now_add=True)
    photo = models.ImageField("Фотография", upload_to='bicycles/')  # in case of name collision suffix autocreated
    verified = models.BooleanField("Данные верифицированы", default=False)  # deprecated
    request_status = models.IntegerField("Статус заявки", default=WAITING, choices=BIKE_STATUS)

    class Meta:
        verbose_name = "велосипед"
        verbose_name_plural = "велосипеды"

    def __str__(self):
        return "Хозяин: {}, велосипед: {} {}".format(self.owner.__str__(), self.manufacturer, self.model)

    def get_absolute_url(self):
        return reverse('bicycle:bicycle_detail', args=[self.id])


# Storage room, contains several places for bicycles
class Storage(models.Model):
    dorm = models.CharField("Расположение", max_length=255, default="Общежитие №6", blank=True, null=True)
    name = models.CharField("Название хранилища", max_length=255, default="Велокомната 6ки")

    class Meta:
        verbose_name = "велохранилище"
        verbose_name_plural = "велохранилища"

    def __str__(self):
        return '{}: {}'.format(self.dorm, self.name)

    # initialize storage with places named by natural numbers. 'num' - count of created places
    def create_places(self, num):
        Place.objects.bulk_create([Place(storage=self, name=str(i)) for i in range(1, num + 1)])

    def randomly_fill(self):
        accepted_bicycles_count = Bicycle.objects.filter(request_status=ACCEPTED, place=None).count()
        if accepted_bicycles_count > self.free_places:
            print("Too many bikes to place in this storage")
            return False
        accepted_bicycles = Bicycle.objects.filter(request_status=ACCEPTED)
        free_places = Place.objects.filter(bicycle=None)
        for bicycle, place in zip(accepted_bicycles, free_places[:accepted_bicycles_count]):
            place.bicycle = bicycle
            place.save()
        print("Done")
        return True

    @property
    def total_places(self):
        return Place.objects.filter(storage=self).count()

    @property
    def free_places(self):
        return Place.objects.filter(storage=self, bicycle=None).count()


# One place in storage, may contain bicycle
class Place(models.Model):
    storage = models.ForeignKey(Storage)
    name = models.CharField("Место", max_length=255)
    bicycle = models.OneToOneField(Bicycle, on_delete=models.SET_NULL, default=None, blank=True, null=True, verbose_name="Велосипед")

    class Meta:
        verbose_name = "место"
        verbose_name_plural = "места"

    def __str__(self):
        return "{}, Место {}".format(self.storage.__str__(), self.name)
