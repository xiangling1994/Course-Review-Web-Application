from django import forms

from .models import addcourse, comment

class PostForm(forms.ModelForm):

    class Meta:
        model = addcourse
        fields = ('subject', 'courseid','prof', 'grade')

class CommentForm(forms.ModelForm):

    class Meta:
        model = comment
        fields = ('user', 'commenttext')
