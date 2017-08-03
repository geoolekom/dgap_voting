from django import forms
from .models import AidRequest, AidDocument


class AidRequestCreateForm(forms.ModelForm):
    document = forms.FileField()

    class Meta:
        model = AidRequest
        fields = ["category", "reason", "req_sum", "urgent"]

    def save(self, commit=True):
        #document = AidDocument(self.cleaned_data['document'])
        #document.save()
        #AidDocument.objects.create(self.cleaned_data['document'])
        return super(AidRequestCreateForm, self).save(commit=commit)