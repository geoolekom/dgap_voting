from django.template import Library, Context
from django.utils.safestring import mark_safe

import logging

from blog.models import Article


logger = logging.getLogger(__name__)
register = Library()


@register.simple_tag
@mark_safe
def article_content(slug):
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
    post = Article.objects.get(slug=slug)
    return post.title


@register.simple_tag
def get_article(slug):
    return Article.objects.get(slug=slug)


# If header_link => title is a link to post detailer view
@mark_safe
@register.inclusion_tag("blog/article_panel.html")
def article_panel(slug, header_link=False, show_creation_time=False):
    post = Article.objects.get(slug=slug)
    return {'article': post,
            'header_link': header_link,
            'show_creation_time': show_creation_time}
