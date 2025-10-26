from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Userprofile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Userprofile.ROLE_CHOICES, required=True, label='Account Type')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Completely remove help texts and password validation hints
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = ''
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})