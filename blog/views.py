from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Article
from .forms import ArticleCreateForm


class ArticleList(generic.ListView):
    model = Article
    template = "blog/article_list"


class ArticleDetail(generic.DetailView):
    model = Article
    template = "blog/article_detail"


# Do we need to create posts NOT from admin panel?
# @login_required()
class ArticleCreate(generic.edit.CreateView):
    model = Article
    form_class = ArticleCreateForm

    def form_valid(self, form):
        response = super(ArticleCreate, self).form_valid(form)
        self.object.author = self.request.user.profile
        self.object.save()
        return response