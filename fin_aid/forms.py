from django import forms
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget

from .models import AidRequest, AidDocument, Category
from profiles.models import UserProfile


class AidRequestCreateForm(forms.ModelForm):
    # TODO rewrite
    document1 = forms.FileField(required=False, label="Документ")
    document2 = forms.FileField(required=False, label="Документ")
    document3 = forms.FileField(required=False, label="Документ")

    class Meta:
        model = AidRequest
        fields = ["category", "reason", "req_sum", "urgent"]

    def __init__(self, *args, **kwargs):
        super(AidRequestCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(show_to_students=True)


class SalaryCreateForm(forms.ModelForm):
    applicant = forms.ChoiceField(
        widget=ModelSelect2Widget(
            model=User,
            search_fields=['userprofile__student_info__fio__icontains'],
            attrs={'class': 'student-select'}
        ), label="Студент"
    )

    class Meta:
        model = AidRequest
        fields = ('applicant', 'req_sum', 'category', 'reason',)
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
            'req_sum': forms.NumberInput(attrs={'class': 'sum_select'})
        }

    def __init__(self, *args, **kwargs):
        super(SalaryCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_senate=True)


AidRequestFormset = forms.modelformset_factory(AidRequest, form=SalaryCreateForm, extra=5)
