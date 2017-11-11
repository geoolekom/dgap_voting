from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.utils import timezone
from django.utils.decorators import method_decorator
from .models import Article
from .forms import ArticleCreateForm


# may be not all stuff, but people with particular rights
def can_view_hidden_post(user): # TODO move to models
    return user.is_authenticated() and (user.is_superuser or user.is_staff)


class ArticleList(generic.ListView):
    """Blog's newsfeed. Shows all visible articles with ``show_in_feed == True``

    Base temlate is ``blog/article_list.html``."""
    model = Article

    def get_context_data(self, **kwargs):
        """Returns list of articles to be shown in feed. See :class:`blog.models.Article` params for details"""
        context = super(ArticleList, self).get_context_data(**kwargs)
        if can_view_hidden_post(self.request.user):
            objects = Article.objects.filter(show_in_feed=True)
        else:
            objects = Article.objects.filter(publish_dttm__lte=timezone.now(), hidden=False, show_in_feed=True)
        context['object_list'] = objects.order_by('-publish_dttm')
        return context


class ArticleDetail(generic.DetailView):
    """Detailed view of article.

    Base template is ``blog/article_detail.html``."""
    model = Article

    def get_context_data(self, **kwargs):
        """Raises 403 error if user can't view this article. See :func:`Article.is_visible`"""
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        if not context["object"].is_visible(self.request.user):
            raise PermissionDenied
        return context


# TODO outdated, articles are created through admin interface
@method_decorator(permission_required('blog.add_article'), name='dispatch')
class ArticleCreate(generic.edit.CreateView):
    model = Article
    form_class = ArticleCreateForm

    def form_valid(self, form):
        response = super(ArticleCreate, self).form_valid(form)
        self.object.author = self.request.user.userprofile
        self.object.save()
        return response
