# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электропочта')
    username = forms.CharField(required=True, label='Логин')
    STATUS_CHOICES = (
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Выберите статус')

    class Meta:
        model = User
        fields = ('username', 'status', 'email', 'password1', 'password2')


# clean email field
def clean_email(self):
    email = self.cleaned_data["email"]
    try:
        User._default_manager.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError('Такой адрес электронной почты уже зарегистрирован.')


# modify save() method so that we can set user.is_active to False when we first create our user
def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.is_active = False  # not active until he opens activation link
        user.save()
    return user
