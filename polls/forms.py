from polls.models import UserProfile
from django import forms
from django.contrib.auth.models import User

from .models import Question


class QuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(QuestionForm, self).__init__(*args, **kwargs)

        answer_type = question.answer_type
        choices = question.choice_set.all()
        if answer_type == Question.ONE:
            self.fields["choices"] = forms.ModelChoiceField(choices, widget=forms.RadioSelect)
        elif answer_type == Question.MANY:
            self.fields["choices"] = forms.ModelMultipleChoiceField(choices, widget=forms.CheckboxSelectMultiple)
        elif answer_type == Question.OWN:
            self.fields["choices"] = forms.CharField(max_length=200)
        else:
            raise ValueError("Incorrect answer type")


QuestionFormset = forms.formset_factory(QuestionForm)


# TODO legacy forms, delete?
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

