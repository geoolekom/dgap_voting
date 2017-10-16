from django import template

from blog.models import Article


register = template.Library()


@register.simple_tag(takes_context=True)
def article_content(context, slug):
    post = Article.objects.get(slug=slug)
    if post.is_django_template:
        return post.rendered_content(context)
    return post.content
article_content.allow_tags = True


@register.simple_tag
def article_title(slug):
    post = Article.objects.get(slug=slug)
    return post.title
article_title.allow_tags = True


@register.simple_tag
def get_article(slug):
    return Article.objects.get(slug=slug)


# If header_link => title is a link to post detailer view
@register.inclusion_tag("blog/article_panel.html")
def article_panel(slug, header_link=False, show_creation_time=False):
    post = Article.objects.get(slug=slug)
    return {'article': post,
            'header_link': header_link,
            'show_creation_time': show_creation_time}
