from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "author", "publish_dttm", "hidden", "show_in_feed", "is_django_template"]
    list_filter = ["author", "hidden", "show_in_feed", "is_django_template"]


admin.site.register(Article, ArticleAdmin)
