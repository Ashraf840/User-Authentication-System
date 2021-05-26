from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class UserRegForm(UserCreationForm):
    class Meta():
        model = MyUser
        fields = ['email', 'company_name', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['company_name'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['phone'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['password1'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['password2'].widget.attrs['style'] = 'width: 550px; height: 35px;'
