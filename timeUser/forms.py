# myProject/myMember/forms.py

from django import forms
from django.db import models
from .models import Profile
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'password1' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False) 
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick', 'email', 'birth_date',]

        widgets = {
            'nick': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'nick': '이름',
            'email': 'e-mail',
            'birth_date': '생일',
        }

class UserCreationMultiForm(MultiModelForm):
    form_classes = {
        'user' : CreateUserForm,
        'profile' : ProfileForm,
    }
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['nick', 'email','birth_date']

        widgets = {
            'nick': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'nick': '이름',
            'email': 'e-mail',
            'birth_date': '생일',
        }
