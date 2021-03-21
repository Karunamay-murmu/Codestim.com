from django import forms
from registration.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'languages']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'your last name'}),
            'bio': forms.Textarea(attrs={'placeholder': 'brief introduction about yourself', 'required': 'True'}),
            'languages': forms.TextInput(attrs={'placeholder': 'programing languages you are working with'})
        }
