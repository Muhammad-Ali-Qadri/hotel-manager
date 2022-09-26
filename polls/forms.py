from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    # fields
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, required=True)
    password_rep = forms.CharField(max_length=20, required=True)
