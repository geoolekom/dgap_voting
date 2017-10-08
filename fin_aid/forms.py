from django import forms
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget

from .models import AidRequest, AidDocument
from profiles.models import UserProfile

class AidRequestCreateForm(forms.ModelForm):
    # TODO rewrite
    document1 = forms.FileField(required=False, label="Документ")
    document2 = forms.FileField(required=False, label="Документ")
    document3 = forms.FileField(required=False, label="Документ")

    class Meta:
        model = AidRequest
        fields = ["category", "reason", "req_sum", "urgent"]

    #def save(self, commit=True):
    #    return super(AidRequestCreateForm, self).save(commit=commit)


class SalaryCreateForm(forms.ModelForm):
    applicant = forms.ChoiceField(
        widget=ModelSelect2Widget(
            model=User,
            search_fields=['userprofile__student_info__fio__icontains']
        )
    )

    class Meta:
        model = AidRequest
        fields = ('category', 'reason', 'req_sum', 'urgent')