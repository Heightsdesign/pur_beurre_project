from django import forms
from django.forms.widgets import TextInput


class UserCreationForm(forms.Form):

    first_name = forms.CharField(
        label="password",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "first_name_input_sub"}),
        required=True,
    )

    email = forms.EmailField(
        label="email",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "email_input_sub"}),
        required=True,
    )

    password = forms.CharField(
        label="password",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "password", "id": "password_input_sub"}),
        required=True,
    )


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="email",
        max_length=150,
        widget=TextInput(attrs={"class": "form-control"}),
        required=True,
    )

    password = forms.CharField(
        label="password",
        max_length=150,
        widget=TextInput(attrs={"class": "form-control"}),
        required=True,
    )
