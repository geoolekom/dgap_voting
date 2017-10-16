from django import forms
from .models import Bicycle, Place


class BicycleCreateForm(forms.ModelForm):

    class Meta:
        model = Bicycle
        fields = ["manufacturer", "model", "info", "photo"]


class BicycleAdminForm(forms.ModelForm):
    place = forms.ModelChoiceField(Place.objects.filter(bicycle=None))

    class Meta:
        model = Bicycle
        exclude = ['image_tag', "photo"]
