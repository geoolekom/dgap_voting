from ckeditor.fields import RichTextField
from django.db import models

from materials.managers import MaterialQuerySet


class MaterialBase(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(verbose_name='заголовок', max_length=128)
    text = RichTextField(verbose_name='текст', max_length=4096)

    is_published = models.BooleanField(verbose_name='опубликован?', default=False)

    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата изменения', auto_now=True)

    objects = MaterialQuerySet.as_manager()

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField(verbose_name='название', max_length=128)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name


class Post(MaterialBase):
    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = '-created_at',


class Article(MaterialBase):
    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    category = models.ForeignKey('Category', verbose_name='категория', related_name='articles')

