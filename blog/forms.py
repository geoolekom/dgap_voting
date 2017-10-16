from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "hidden", "content"]


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        models = Article
        widgets = {
            'content': CKEditorWidget
        }
        # exclude = ['author']
