from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
import re
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ✅ Use your model here
        fields = ("email", "username", "password1", "password2")  # No 'username' if not using AbstractUser


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)


def validate_georgian_phone(value):
    if not re.match(r'^(?:\+995)?5\d{8}$', value):
        raise ValidationError('Enter a valid Georgian phone number.')

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter address'
    }))
    phone = forms.CharField(
        max_length=15,
        validators=[validate_georgian_phone],
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'pattern': r'^(?:\+995)?5\d{8}$',
            'inputmode': 'numeric',
            'placeholder': 'e.g. +995599123456 or 599123456',
            'class': 'form-control',
        })
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes'
        })
    )