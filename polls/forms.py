from polls.models import UserProfile
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name')

class UserProfileFormReduced(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('room',)

class UserProfileForm(UserProfileFormReduced):
    cardnumber = forms.CharField(min_length=5, max_length=5, required=True)
    class Meta(UserProfileFormReduced.Meta):
        fields = UserProfileFormReduced.Meta.fields + ('cardnumber',)

