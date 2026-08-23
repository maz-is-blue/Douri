from django import forms

from .models import FormSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Phone (optional)'}),
            'subject': forms.Select(attrs={'class': 'field'}),
            'message': forms.Textarea(
                attrs={'class': 'field', 'placeholder': 'How can we help?', 'rows': 6}
            ),
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Phone'}),
            'message': forms.Textarea(
                attrs={'class': 'field', 'placeholder': "Tell us how you'd like to help", 'rows': 4}
            ),
        }


class SupportForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'Email'}),
            'message': forms.Textarea(
                attrs={'class': 'field', 'placeholder': 'Your message', 'rows': 4}
            ),
        }
