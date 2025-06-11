# blog/forms.py
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'categories', 'tags',
                  'slug', 'cover_image', 'status', 'references']

        exclude = ['slug'] 
