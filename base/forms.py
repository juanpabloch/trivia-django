from django.contrib.auth import get_user_model
from django import forms
from base import models
from base.services import utils

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    
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
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput())
    

class OptionsForm(forms.Form):
    category = forms.ChoiceField(choices=utils.get_categories(), label='Categoria')
    difficulty = forms.ChoiceField(choices=utils.get_difficulty(), label='Dificultad')
