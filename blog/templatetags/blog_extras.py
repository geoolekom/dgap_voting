"""Some custom templatetags simplifying article rendering in templates"""
from django.template import Library, Context
from django.utils.safestring import mark_safe
import logging

from blog.models import Article


logger = logging.getLogger(__name__)
register = Library()


@register.simple_tag
@mark_safe
def article_content(slug):
    """Simple temlatetag to retrieve article's content by slug. If article is django template, it's content is rendered"""
    try:
        post = Article.objects.get(slug=slug)
        if post.is_django_template:
            return post.rendered_content
        return post.content
    except Article.DoesNotExist as e:
        logger.exception(e)
        return ""


@register.simple_tag
@mark_safe
def article_title(slug):
    """Simple temlatetag to retrieve article's content by slug. If article is django template, it's content is rendered"""
    post = Article.objects.get(slug=slug)
    return post.title


@register.simple_tag
def get_article(slug):
    """Templatetag that returns article (variable with all article data) by it's slug.

    Can be used in templates to manualy display article on a page

    :param str slug: Article's slug
    :return Article: :class:`blog.models.Article` instance"""
    return Article.objects.get(slug=slug)


@register.inclusion_tag("blog/article_panel.html")
def article_panel(slug, header_link=False, show_creation_time=False):
    """Incluision tag that renders article content. Base template is ``blog/article_panel. Currently is basic bootstrap panel

    This templatetag is used in ``blog/article_list.html``, ``blog/article_detail.html``.

    :param str slug: article's slug
    :param bool header_link: If ``True`` then article header is a link to :class:`blog.views.ArticleDetail`
    :param bool show_creation_time: If ``True`` then publication datetime is shown.
    :return: rendered article template
    """
    post = Article.objects.get(slug=slug)
    return {'article': post,
            'header_link': header_link,
            'show_creation_time': show_creation_time}
