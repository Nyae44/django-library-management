# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'member', 'return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'member', 'return_date','actual_return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_return_date': forms.DateInput(attrs={'type': 'date'}),
        }