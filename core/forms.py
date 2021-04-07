from django import forms


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
