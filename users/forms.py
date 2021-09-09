from django import forms
from django.forms.widgets import TextInput

class UserCreationForm(forms.Form):

    first_name = forms.CharField(
        label = 'first_name',
        max_length = 150,
        widget = forms.TextInput(attrs={'class' : 'form-control'}),
        required = True
    )

    user_name = forms.CharField(
        label = 'user_name',
        max_length = 150,
        widget = forms.TextInput(attrs={'class' : 'form-control'}),
        required = True
    )

    email = forms.EmailField(
        label = 'email',
        max_length = 150,
        widget = forms.TextInput(attrs={'class' : 'form-control'}),
        required = True
    )

    password = forms.CharField(
        label = 'user_name',
        max_length = 150,
        widget = forms.TextInput(attrs={'class' : 'form-control'}),
        required = True
    )

class LoginForm(forms.Form):

    user_name = forms.CharField(
        label = 'user_name',
        max_length = 150,
        widget = forms.TextInput(attrs={'class' : 'form-control'}),
        required = True
    )

    password = forms.CharField(
        label = 'user_name',
        max_length = 150,
        widget = forms.TextInput(attrs={'class' : 'form-control'}),
        required = True
    )

