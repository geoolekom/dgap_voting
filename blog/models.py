from django.db import models
from django.contrib.auth.models import User


from profiles.models import UserProfile


class Article(models.Model):
    title = models.CharField(max_length=255, default=None, blank=True, null=True)  # заголовок поста
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    publish_dttm = models.DateTimeField('Publish datetime', auto_now_add=True)  # дата публикации
    content = models.TextField(max_length=10000) # текст поста

    def __str__(self):
        return "{} posted: {} on {}".format(self.author.__str__(), self.title, self.publish_dttm.__str__())