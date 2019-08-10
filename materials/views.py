from django.views.generic import TemplateView, DetailView, ListView

from materials.models import Category, Post, Article


class Index(TemplateView):
    template_name = 'materials/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.public().order_by('-created_at')[:3]
        return context


class CategoryDetail(DetailView):
    template_name = 'materials/category_detail.html'
    model = Category


class PostList(ListView):
    template_name = 'materials/post_list.html'
    model = Post
    queryset = Post.objects.public()
    paginate_by = 20
    ordering = '-published_at',


class PostDetail(DetailView):
    template_name = 'materials/post_detail.html'
    model = Post
    queryset = Post.objects.public()


class ArticleDetail(DetailView):
    template_name = 'materials/article_detail.html'
    model = Article
    queryset = Article.objects.public()
