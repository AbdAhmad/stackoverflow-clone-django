from django import forms
from .models import Profile, Question, Answer
from django import forms
from crispy_forms.helper import FormHelper


class AnswerForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_show_labels = False

    class Meta:
        model = Answer
        fields = ['ans']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'location', 'about_me']