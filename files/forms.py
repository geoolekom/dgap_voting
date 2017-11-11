from django import forms
from django.forms import formset_factory

class FileForm(forms.Form):
    file = forms.FileField(required=False)

FilesFormSet = formset_factory(FileForm, extra=1)