from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User
from . forms import UserCreationForm
# Register your models here.

admin.site.register(User)

""" 
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = UserAdmin
"""

