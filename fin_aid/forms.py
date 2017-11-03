from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget

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


class AidRequestAdminForm(forms.ModelForm):
    THIS = 1
    NEXT = 2
    FOLLOWING = 3
    MONTHS = [(THIS, "Ближайший месяц"),
              (NEXT, "Следующий месяц"),
              (FOLLOWING, "Через месяц"),]
    month_of_payment = forms.ChoiceField(choices=MONTHS, label="Месяц выплаты")

    class Meta:
        model = AidRequest
        exclude = ["examination_dttm"]
        widgets = {
            'applicant': ModelSelect2Widget(model=User,
                                            search_fields=['userprofile__student_info__fio__icontains', 'first_name', 'last_name'],
                                            attrs={'data-width': '30em'}
                                            ),
            'author': ModelSelect2Widget(model=User,
                                         search_fields=['userprofile__student_info__fio__icontains', 'first_name', 'last_name'],
                                         attrs={'data-width': '30em'}
                                         )
        }
