from django.contrib.auth import login, authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from core.forms import LoginForm
from core.models import User

class MyBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, *args, **kwargs):
        if email is None or password is None:
            return
        try:
            user = User.objects.get(email=email)
            if user:
                if check_password(password, user.password):
                    return user
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
class LoginView(View):
    template_name = 'core/html/login.html'
    form_class = LoginForm
    context = {}
    success_url = 'core-index'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                a = login(request, user, backend='core.auth_views.MyBackend')
                return redirect(reverse(self.success_url))
            else:
                self.context['error'] = True
                return render(request, self.template_name, self.context)

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass



class LogoutView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class ResetView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class ResetSuccessView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class ResetConfirmView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
