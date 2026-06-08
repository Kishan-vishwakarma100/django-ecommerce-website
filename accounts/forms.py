from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()

        # ✅ Normal username rule
        if not re.match(r'^[a-zA-Z0-9._@]+$', username):
            raise forms.ValidationError(
                "Username can only contain letters, numbers, ., _, @"
            )

        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()

        if commit:
            user.save()

        return user