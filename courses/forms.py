from cProfile import label

from django import forms
from django.core.validators import RegexValidator, MinLengthValidator
from .models import User, Application

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]+$', 'Только латинские буквы и цифры.'),
            MinLengthValidator(6, 'Логин должен содержать минимум 6 символов.')
        ]
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8, 'Пароль должен содержать минимум 8 символов.')]
    )
    fio = forms.CharField(
        label='ФИО',
        validators=[RegexValidator(r'^[А-Яа-яЁё\s]+$', 'Только кириллица и пробелы.')]
    )
    birth_date = forms.CharField(
        label='Дата рождения',
        validators=[RegexValidator(r'^\d{2}\.\d{2}\.\d{4}$', 'Формат: ДД.ММ.ГГГГ')]
    )
    phone = forms.CharField(
        label='Номер телефона'
    )
    email = forms.EmailField(
        label='Электронная почта (E-mail)'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'fio', 'birth_date', 'phone', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ApplicationForm(forms.ModelForm):
    start_date = forms.CharField(
        validators=[RegexValidator(r'^\d{2}\.\d{2}\.\d{4}$', 'Формат: ДД.ММ.ГГГГ')]
    )

    class Meta:
        model = Application
        fields = ['transport_type', 'start_date', 'payment_method']