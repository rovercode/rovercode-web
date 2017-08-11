"""Mission Control forms."""
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Fields for modifying post details."""

    class Meta:
        """Meta class."""

        model = Post
        fields = '__all__'
