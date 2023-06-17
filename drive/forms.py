from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Folder, Files


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder_name', 'is_important']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file_name', 'file_upload')
