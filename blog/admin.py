from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "publish_dttm", "hidden"]
    list_filter = ["author", "publish_dttm", "hidden"]

admin.site.register(Article, ArticleAdmin)
