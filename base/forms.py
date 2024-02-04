from django.contrib.auth import get_user_model
from django import forms
from base import models
from base.services import utils

User = get_user_model()

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget= forms.EmailInput(
        attrs={
            "placeholder": "Email",
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget = forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control"
        }
    ))
    confirm_password = forms.CharField(widget = forms.PasswordInput(
        attrs={
            "placeholder": "Confirm password",
            "class": "form-control"
        }
    ))
    
    class Meta:
        model = User
        fields = ("email", "password", "confirm_password")
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
      
        
class LoginForm(forms.Form):
    email = forms.EmailField(widget= forms.EmailInput(
        attrs={
            "placeholder": "Email",
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget = forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control"
        }
    ))
