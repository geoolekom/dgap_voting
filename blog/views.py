from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Article
from .forms import ArticleCreateForm


# may be not all stuff, but people with particular rights
def can_view_hidden_post(user): # TODO move to models
    return user.is_authenticated() and (user.is_superuser or user.is_staff)


class ArticleList(ListView):
    template_name = 'blog/article_list.html'
    model = Article
    ordering = '-publish_dttm'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if can_view_hidden_post(user):
            return queryset.filter(show_in_feed=True)
        else:
            return queryset.filter(publish_dttm__lte=timezone.now(), hidden=False, show_in_feed=True)


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
