from django import forms
from .models import Comment, Contact, Subscriber
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'comment-body',
                    'rows': 10,
                    'placeholder': 'Write a comment here...'
                }
            )
        }


class ContactForm(forms.ModelForm):
    class Meta():
        model = Contact
        exclude = ['message_type']
        labels = {
            'name': _('Your Name(required)'),
            'email': _('Your Email Address(required)'),
            'message': _('Your Message (required)')
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your name',
                    'autocomplete': 'off'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email',
                    'autocomplete': 'off'

                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'placeholder': 'Enter the subject',
                    'autocomplete': 'off'

                }
            ),
            'message': forms.Textarea(
                attrs={
                    'placeholder': 'Write down your message',
                    'rows': 15
                }
            )
        }


class SubscriberForm(forms.ModelForm):
    class Meta():
        model = Subscriber
        fields = ['subscriber_email']

        widgets = {
            'subscriber_email': forms.EmailInput(
                attrs={
                    'class': 'email-input',
                    'placeholder': 'Enter your email',
                    'required': True,
                    'autocomplete': 'off'
                }
            )
        }
