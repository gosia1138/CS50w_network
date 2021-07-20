from django import forms
from .models import User, Profile, Post

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs = {
                'placeholder': 'What\'s up?',
                'class': 'form-control',
                'rows': 5,
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['followed']
