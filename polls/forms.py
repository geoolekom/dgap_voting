from polls.models import Choice, Poll, UserHash, UserProfile
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name')
 #       widgets = {
 #           'username': forms.TextInput(attrs={'readonly': True}),
 #       }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #exclude = ('user', 'approval')
        fields = ('room', 'cardnumber',)

class UserProfileFormReduced(forms.ModelForm):
    class Meta:
        model = UserProfile
        #exclude = ('user', 'approval')
        fields = ('room',)

