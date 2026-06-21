from django import forms
from django.contrib.auth import authenticate

from team_finder.validators import validate_github_url, validate_phone
from users.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Неверный email или пароль.')
            self._user = user
        return cleaned_data

    def get_user(self):
        return self._user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_github_url(self):
        value = self.cleaned_data.get('github_url', '')
        validate_github_url(value)
        return value

    def clean_phone(self):
        value = self.cleaned_data.get('phone', '')
        validate_phone(value)
        return value
