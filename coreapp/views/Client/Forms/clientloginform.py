# Import the forms library to create forms
from django import forms

# Import the CaptchaField from 'django-simple-captcha'
from captcha.fields import CaptchaField

from  django.core.validators import RegexValidator
from coreapp.models import *
# Create form class for the Registration form

class LoginForm(forms.Form):
	name = forms.CharField()
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput) # Set the widget to
