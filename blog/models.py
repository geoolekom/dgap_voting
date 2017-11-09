from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template import Context, Template

from profiles.models import UserProfile


# TODO change author model to user instead of userprofile
class Article(models.Model):
    """Describes model for storing articles. Can render it's content as Django template.

    :param models.SlugField slug: User-friendly url for stored article
    :param models.CharField title: Article title
    :param models.ForeignKey author: Article author, relates to :class:`profiles.models.UserProfile`
    :param models.DateTimeField publish_dttm: Publication Date and time. Auto populated at article creation.
    :param models.TextField content: Article content. Can store html (including Django templates)
    :param models.BooleanField hidden: `True` if article is hidden from regular users. See :func:`is_visible`.
    :param models.BooleanField show_in_feed: `True` if article should appear in feeds such as :class:`blog.views.ArticleList`
    :param models.BooleanField is_django_template: `True` if article should be rendered as Django template. See :func:`rendered_content`
    """
    slug = models.SlugField("URL")
    title = models.CharField("Заголовок", max_length=255, default=None, blank=True, null=True)  # заголовок поста
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    publish_dttm = models.DateTimeField('Дата публикации', auto_now_add=True)  # дата публикации
    content = models.TextField("Контент", max_length=20000) # текст поста
    hidden = models.BooleanField("Скрытый", default=False)
    show_in_feed = models.BooleanField("ПОказывать в ленте", default=True)
    is_django_template = models.BooleanField("Шаблон Django", default=False)

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"

    @property
    def rendered_content(self, context=Context()):
        """ Renders `self.content` as Django template.

        :param Context context: Additional context to be passed to template
        :return: Rendered template
        """
        template = Template(self.content)
        return template.render(context)

    def get_absolute_url(self):
        """ Get URL of this article

        :return: URL
        """
        return reverse('blog:article_detail', args=[self.slug])

    def is_visible(self, user: User):
        """ Checks if specified user van ciew this post. E.g. post is published, of user is staff & so on

        :param User user: User to be checked
        :return: `True` if `User` can view this post, else `False`
        :rtype: bool
        """
        return self.publish_dttm <= timezone.now() and not self.hidden \
               or (user.is_authenticated() and (user.is_superuser or user.is_staff))

    def __str__(self):
        return "{} posted: {} on {}".format(self.author.__str__(), self.title, self.publish_dttm.__str__())

