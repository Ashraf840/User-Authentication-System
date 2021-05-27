from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.contrib.auth import authenticate


class UserRegForm(UserCreationForm):
    class Meta():
        model = MyUser
        fields = ['email', 'username', 'company_name', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['username'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        # self.fields['username'].widget.attrs['value'] = 'Default Value'
        self.fields['company_name'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['phone'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['password1'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['password2'].widget.attrs['style'] = 'width: 550px; height: 35px;'


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta():
        model = MyUser
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            # Raise authentication error
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials! Please insert correct email & password.")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['style'] = 'width: 550px; height: 35px;'
        self.fields['password'].widget.attrs['style'] = 'width: 550px; height: 35px;'
