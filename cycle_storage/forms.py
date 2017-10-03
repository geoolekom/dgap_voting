from django import forms
from .models import Bicycle


class BicycleCreateForm(forms.ModelForm):

    class Meta:
        model = Bicycle
        fields = ["manufacturer", "model", "info", "photo"]
