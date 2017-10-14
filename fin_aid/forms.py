from django import forms
from django.utils import timezone
from .models import AidRequest, MonthlyData


class AidRequestCreateForm(forms.ModelForm):
    # TODO rewrite
    document1 = forms.FileField(required=False, label="Документ")
    document2 = forms.FileField(required=False, label="Документ")
    document3 = forms.FileField(required=False, label="Документ")

    class Meta:
        model = AidRequest
        fields = ["category", "reason", "req_sum", "urgent"]


class SelectExportMonthForm(forms.Form):
    year = forms.IntegerField(label="Год", initial=timezone.now().year, min_value=2000, max_value=3000)
    month = forms.ChoiceField(label="Месяц", initial=timezone.now().month, choices=MonthlyData.MONTH)
