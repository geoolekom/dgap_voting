from django.contrib import admin

from materials.models import Category, Post, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug',


class MaterialAdmin(admin.ModelAdmin):
    list_display = 'title', 'is_published',
    list_filter = 'is_published',
    search_fields = 'title', 'text',


@admin.register(Post)
class PostAdmin(MaterialAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(MaterialAdmin):
    pass
