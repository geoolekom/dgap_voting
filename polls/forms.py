from polls.models import UserProfile
from django import forms
from django.contrib.auth.models import User

from .models import Question

"""
class QuestionForm(forms.Form):

    def __init__(self, question: Question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.question = question.question
        answer_type = question.answer_type
        choices = question.choice_set.all()
        if answer_type == Question.ONE:
            field = forms.ModelChoiceField(choices, widget=forms.RadioSelect)
        elif answer_type == Question.MANY:
            field = forms.ModelMultipleChoiceField(choices, widget=forms.CheckboxSelectMultiple)
        elif answer_type == Question.OWN:
            field = forms.CharField(max_length=200)
        else:
            raise ValueError("Incorrect answer type")
        self.fields["choices"] = field


class PollForm(forms.Form):

    def __init__(self, questions, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        for question in questions:
            self.question = question.question
            answer_type = question.answer_type
            choices = question.choice_set.all()
            if answer_type == Question.ONE:
                field = forms.ModelChoiceField(choices, widget=forms.RadioSelect)
            elif answer_type == Question.MANY:
                field = forms.ModelMultipleChoiceField(choices, widget=forms.CheckboxSelectMultiple)
            elif answer_type == Question.OWN:
                field = forms.CharField(max_length=200)
            else:
                raise ValueError("Incorrect answer type")
            self.fields["choices"] = field


class QuestionFormset(forms.BaseFormSet):
    def __init__(self, questions):
        data = {
            'form-TOTAL_FORMS': str(len(questions)),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        data.update({'form-{}-question': })

QuestionFormset = forms.formset_factory(QuestionForm)
"""

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

