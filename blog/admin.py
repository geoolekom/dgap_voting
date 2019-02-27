from django.contrib import admin
from .models import Article
from .forms import ArticleAdminForm


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """:class:`Article` admin class. New articles are created by moderators via this page"""
    prepopulated_fields = {"slug": ("title",)}
    form = ArticleAdminForm
    list_display = ["title", "author", "publish_dttm", "hidden", "show_in_feed", "is_django_template"]
    list_filter = ["author", "hidden", "show_in_feed", "is_django_template"]
    readonly_fields = ['author']

    def save_model(self, request, obj, form, change):
        "Sets object author as `request.user`"
        obj.author = request.user.userprofile
        obj.save()
        super(ArticleAdmin, self).save_model(request, obj, form, change)
