from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from profiles.models import UserProfile


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=255, default=None, blank=True, null=True)  # заголовок поста
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    publish_dttm = models.DateTimeField('Дата публикации', auto_now_add=True)  # дата публикации
    content = models.TextField("Контент", max_length=10000) # текст поста
    hidden = models.BooleanField("Скрытый", default=False)

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.id])

    def is_visible(self, user):
        return self.publish_dttm <= timezone.now() and not self.hidden \
               or (user.is_authenticated() and (user.is_superuser or user.is_staff))

    def __str__(self):
        return "{} posted: {} on {}".format(self.author.__str__(), self.title, self.publish_dttm.__str__())