from django import forms
from django.forms import CharField, Form, PasswordInput
from .models import course, comment, account

class PostForm(forms.ModelForm):

    class Meta:
        model = course
        fields = ('subject', 'courseid', 'grade')

class CommentForm(forms.ModelForm):

    class Meta:
        model = comment
        fields = ('commenttext',)

class AccountForm(forms.ModelForm):

    password = CharField(widget=PasswordInput())
    class Meta:
        model = account
        fields = ('username', 'password', 'email')

class LoginForm(forms.ModelForm):

    password = CharField(widget=PasswordInput())
    class Meta:
        model = account
        fields = ('username', 'password')

class RatingFormHelpfulness(forms.Form):
    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    rating_field_helpfulness = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class RatingFormClarity(forms.Form):
    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    rating_field_clarity = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class RatingFormEasiness(forms.Form):
    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    rating_field_easiness = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class RatingFormTextbook(forms.Form):
    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    rating_field_textbook = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)


class SearchForm(forms.Form):
    search_handle = forms.CharField(label='Search Handle', max_length=100)

class DeleteForm(forms.Form):
    delete_handle = forms.CharField(label='Delete Handle', max_length=100)

