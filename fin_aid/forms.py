from django import forms
from .models import AidRequest, AidDocument


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