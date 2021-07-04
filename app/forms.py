from django import forms
from .models import User, Customer
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation


class SignupForm(UserCreationForm):
    password1 = forms.CharField( label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField( label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email Id", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}))
    new_password1 = forms.CharField(label='New Password',strip=False , widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))

class MyPassResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'passwordresetautocomplete':'email'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'})
        }