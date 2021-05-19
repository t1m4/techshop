import datetime

from django import forms
from django.forms import DateInput

SELECT_CHOICES = [('price', 'Цена (низкая)'), ('-price', 'Цена (высокая)'), ('-name', 'Название А-Я'), ('name', 'Название Я-А')]
class LoginForm(forms.Form):
    email = forms.EmailField(label="Почта")
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    double_password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

class ResetForm(forms.Form):
    email = forms.EmailField(label='Почта')

class PasswordResetEmailForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    double_password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

class SupportForm(forms.Form):
    name = forms.CharField(max_length=40, label='Имя')
    fio = forms.CharField(max_length=40, label='Фамилия')
    email = forms.EmailField(label='Почта')
    title = forms.EmailField(label='Заголовок')
    message = forms.CharField(widget=forms.Textarea, max_length=1024, label='Напишите сообщение')


class ProductForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=100, label='Количество')

class BasketForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=100, label='Количество')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255, label='Количество', required=False)

class SortForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.Select, choices=SELECT_CHOICES, label="Сортировка")

class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    address = forms.CharField(max_length=50, label='Адрес')

from django.contrib.admin import widgets
class OrderSearchForm(forms.Form):
    # start_day = forms.DateField(initial=datetime.date.today, widget=forms.DateInput, label='Дата начала')
    start_day = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=range(2020, 2030)), label='Дата начала')
    end_day = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=range(2020, 2030)), label='Дата конца')
    category = forms.CharField(max_length=100, label='Категория', required=False)