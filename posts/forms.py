from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=165,)
    # body = forms.Textarea()

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': TinyMCE()
        }
        exclude = ['user', 'created_at']

# Dans votre fichier forms.py

from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
