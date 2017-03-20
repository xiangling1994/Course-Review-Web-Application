from django import forms
from django.forms import CharField, Form, PasswordInput
from .models import addcourse, comment, user

class PostForm(forms.ModelForm):

    class Meta:
        model = addcourse
        fields = ('subject', 'courseid', 'grade')

class CommentForm(forms.ModelForm):

    class Meta:
        model = comment
        fields = ('commenttext',)

class UserForm(forms.ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta:
        model = user
        fields = ('username', 'password', 'email')

class LoginForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = user
        fields = ('username', 'password')
