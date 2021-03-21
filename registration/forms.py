from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate

from .models import User
from .validator import PasswordValidation

class Signup(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input'}))
    password2 = forms.CharField(
        label='Confirm Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Username(Jhon02)", 'autocomplete': 'off', 'class': 'input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email(Example@email.com)', 'autocomplete': 'off', 'class': 'input'})
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'User with this username already exists.')

        return username

    def clean_email(self):
        user_email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=user_email).exists():
            raise forms.ValidationError('User with this email already exists.')

        return user_email.lower()

    def clean_password1(self):
        pass1 = self.cleaned_data['password1']
        validPassword = PasswordValidation(self, pass1)

        if validPassword.validate() is not True:
            raise forms.ValidationError(
                "Password Invalid, please choose a valid password")

        return pass1

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError("Passwords didn't match.")

        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class Login(forms.Form):
    email = forms.EmailField(
        label="email", widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'class': 'input'}), required=True)
    password = forms.CharField(
        label="password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'input'}), required=True)

    def clean_email(self):
        email = self.cleaned_data['email']

        return email.lower()

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(
                    "Invaild credentials. Please enter correct information")

        return super(Login, self).clean(*args, **kwargs)


class ResetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        new_password = self.cleaned_data['new_password1']
        validPassword = PasswordValidation(self, new_password)

        if validPassword.validate() is not True:
            raise forms.ValidationError(
                "Password Invalid, please choose a valid password")

        return new_password

    def clean_new_password2(self):
        new_password = self.cleaned_data.get('new_password1')
        confirm_new_password = self.cleaned_data.get('new_password2')

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError("Passwords didn't match.")

        return confirm_new_password
