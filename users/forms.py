from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Enter password',
                                help_text=None, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                help_text=None, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input100'}),
            'password1': forms.PasswordInput(attrs={'class': 'input100'}),
            'password2': forms.PasswordInput(attrs={'class': 'input100'}),
            'email': forms.EmailInput(attrs={'class': 'input100'}),
        }
        help_texts = {k: "" for k in fields}
