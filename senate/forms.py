from django import forms
from .models import Issue, Event, Category

from django_select2.forms import ModelSelect2Widget


class IssueCreateForm(forms.ModelForm):
    issue_descr = forms.CharField(label="Описание", max_length=Event.MAX_INFO_LEN, widget=forms.Textarea(attrs={'rows': 5}))
    # TODO rewrite
    photo1 = forms.ImageField(required=False, label="Фотография")
    photo2 = forms.ImageField(required=False, label="Фотография")
    photo3 = forms.ImageField(required=False, label="Фотография")

    class Meta:
        model = Issue
        fields = ["name", "category", "want_to_help"]
        widgets = {'category': ModelSelect2Widget(model=Category, queryset=Category.objects.all())}


class DeptEventCreateForm(forms.ModelForm):
    photo1 = forms.ImageField(required=False, label="Фотография")
    photo2 = forms.ImageField(required=False, label="Фотография")
    photo3 = forms.ImageField(required=False, label="Фотография")

    class Meta:
        model = Event
        fields = ["cls", "info", "new_status", "new_dept"]
        widgets = {"info": forms.Textarea}


class UserEventCreateForm(forms.ModelForm):
    photo1 = forms.ImageField(required=False, label="Фотография")
    photo2 = forms.ImageField(required=False, label="Фотография")
    photo3 = forms.ImageField(required=False, label="Фотография")

    class Meta:
        model = Event
        fields = ["info"]
        widgets = {"info": forms.Textarea}
