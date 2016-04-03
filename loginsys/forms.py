from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput
                             (attrs={'placeholder': 'Электронный адрес'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
