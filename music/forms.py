from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from validate_email import validate_email


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            return email
        raise ValidationError('Enter a valid email')
