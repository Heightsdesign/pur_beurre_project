from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.forms import ModelForm

class UserCreationForm(auth_forms.UserCreationForm):
    
    class Meta(auth_forms.UserCreationForm.Meta):
        #New user creation form
        model = get_user_model()
        # add fields variable to change form fields
        # fields = "Enter fields"

class UserChangeForm(auth_forms.UserChangeForm):

    class Meta(auth_forms.UserChangeForm.Meta):
        model = get_user_model()

class AdminForm(ModelForm):
    model = get_user_model()