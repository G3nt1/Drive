from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Folder, Files, UserPreference


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
        fields = ['folder_name']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file_upload',)


class FileUpdateForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file_upload', 'file_name')


class SharedForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['user']
        labels = {
            'user': 'Select User',
        }


class UserPreForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ('view_mode', 'theme_mode',)
        widgets = {
            'view_mode': forms.RadioSelect(attrs={'class': 'view-mode-radio'}),
            'theme_mode': forms.RadioSelect(attrs={'class': 'theme-mode-radio'}),
        }


class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField()
