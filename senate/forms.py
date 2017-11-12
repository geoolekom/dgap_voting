from django import forms
from .models import Issue, Event

class IssueCreateForm(forms.ModelForm):
    issue_descr = forms.CharField(label="Описание", max_length=Event.MAX_INFO_LEN, widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Issue
        fields = ["name", "category", "want_to_help"]


class DeptEventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["cls", "info", "new_status", "new_dept"]
        widgets = {"info": forms.Textarea}


class UserEventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["info"]
        widgets = {"info": forms.Textarea}
