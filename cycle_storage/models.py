from django.db import models
from profiles.models import UserProfile
from django.core.urlresolvers import reverse


def bike_photo_path(instance, filename):
    return "bicycles/user{}_{}".format(instance.user.id, filename)


class Bicycle(models.Model):
    owner = models.ForeignKey(UserProfile, blank=True, null=True)
    manufacturer = models.CharField("Производитель", max_length=255, default="Неизвестно", blank=True, null=True)
    model = models.CharField("Модель", max_length=255, default="Неизвестно", blank=True, null=True)
    add_dttm = models.DateTimeField('Publish datetime', auto_now_add=True)
    photo = models.ImageField("Фотография", upload_to=bike_photo_path)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Велосипед"
        verbose_name_plural = "Велосипеды"

    def __str__(self):
        return "Хозяин: {}, велосипед: {} {}".format(self.owner.__str__(), self.manufacturer, self.model)

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.id])


# Storage room, contains several places for bicycles
class Storage(models.Model):
    dorm = models.CharField("Общежитие", max_length=255, default="6", blank=True, null=True)
    name = models.CharField("Номер места", max_length=255, default="Велокомната 6ки")

    class Meta:
        verbose_name = "Велохранилище"
        verbose_name_plural = "Велохранилища"

    def __str__(self):
        return 'Общежитие {}, {}'.format(self.dorm, self.name)

    # initialize storage with places named by natural numbers. 'num' - count of created places
    def create_places(self, num):
        Place.objects.bulk_create([Place(storage=self, name=str(i)) for i in range(1, num + 1)])

    @property
    def total_places(self):
        return Place.objects.filter(storage=self).count()

    @property
    def free_places(self):
        return Place.objects.filter(storage=self, bicycle=None).count()


# One place in storage, may contain bicycle
class Place(models.Model):
    storage = models.ForeignKey(Storage)
    name = models.CharField(max_length=255)
    bicycle = models.OneToOneField(Bicycle, on_delete=models.SET_NULL, default=None, blank=True, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return "{}, Место {}".format(self.storage.__str__(), self.name)
