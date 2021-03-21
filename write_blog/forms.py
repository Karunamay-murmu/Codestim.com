from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from blog.models import Categorie, Draft


def postForm(modelName):
    class WritePost(forms.ModelForm):
        category = forms.ModelChoiceField(
            queryset=Categorie.objects.all(), empty_label="Choose Category", to_field_name="name")

        class Meta:
            model = modelName
            fields = ['category', 'title',
                      'body', 'featured_image', 'tags', 'meta_title', 'slug', 'meta_description']

            widgets = {
                'title': forms.TextInput(attrs={
                    'placeholder': 'Enter title here',
                    'autocomplete': 'off',
                }),
                'tags': forms.TextInput(attrs={
                    'placeholder': 'Enter tags (separate by comma)',
                    'autocomplete': 'off',
                }),
                'meta_title': forms.TextInput(attrs={
                    'placeholder': 'Meta title',
                    'autocomplete': 'off'
                }),
                'slug': forms.TextInput(attrs={
                    'placeholder': 'Parmalink',
                    'autocomplete': 'off'
                }),
                'meta_description': forms.Textarea(attrs={
                    'placeholder': 'Meta description',
                    'autocomplete': 'off',
                    'rows': 10
                })
            }

    return WritePost
