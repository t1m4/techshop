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