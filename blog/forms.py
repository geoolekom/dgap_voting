"""Forms for article app"""

from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Article


# TODO legacy, articles are created through admin interface
class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "hidden", "content"]


class ArticleAdminForm(forms.ModelForm):
    """Basic form for article change_view. Replaces text input with WYSISYG editor"""
    class Meta:
        models = Article
        widgets = {
            'content': CKEditorWidget
        }
        # exclude = ['author']
