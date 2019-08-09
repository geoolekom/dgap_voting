from django.views.generic import TemplateView, DetailView

from materials.models import Category, Post


class Index(TemplateView):
    template_name = 'materials/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.public().order_by('-created_at')[:5]
        return context


class CategoryDetail(DetailView):
    template_name = 'materials/category_detail.html'
    model = Category
