from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.utils import timezone
from .models import Article
from .forms import ArticleCreateForm


# may be not all stuff, but people with particular rights
def can_view_hidden_post(user):
    return user.is_authenticated() and (user.is_superuser or user.is_staff)


class ArticleList(generic.ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        if can_view_hidden_post(self.request.user):
            objects = Article.objects.filter(show_in_feed=True)
        else:
            objects = Article.objects.filter(publish_dttm__lte=timezone.now(), hidden=False, show_in_feed=True)
        context['object_list'] = objects.order_by('-publish_dttm')
        return context


class ArticleDetail(generic.DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        if not context["object"].is_visible(self.request.user):
            raise PermissionDenied
        return context


# TODO decorator doesn't work, fix
# @permission_required('blog.add_article')
class ArticleCreate(generic.edit.CreateView):
    model = Article
    form_class = ArticleCreateForm

    def form_valid(self, form):
        response = super(ArticleCreate, self).form_valid(form)
        self.object.author = self.request.user.userprofile
        self.object.save()
        return response
