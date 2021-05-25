from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class UserRegForm(UserCreationForm):
    class Meta():
        model = MyUser
        fields = ['email', 'company_name', 'phone', 'password1', 'password2']
