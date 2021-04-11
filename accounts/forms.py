from accounts.models import MyUser
from django.contrib.auth.forms import UserCreationForm

from django import forms

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())
	otp = forms.CharField(max_length = 20,required = False)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("email",)
