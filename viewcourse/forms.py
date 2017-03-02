from django import forms

from .models import addcourse

class PostForm(forms.ModelForm):

    class Meta:
        model = addcourse
        fields = ('subject', 'courseid','prof', 'grade')
