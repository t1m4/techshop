import uuid

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import password_changed
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from core.forms import LoginForm, RegisterForm, ResetForm, PasswordResetEmailForm
from core.models import User
from core.tool import get_object_or_none


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
    context = { 'errors': ''}
    success_url = 'core-index'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class()
        self.context['form'] = form
        self.context['errors'] = ''
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
                # login(request, user, backend='core.auth_views.MyBackend')
                a = login(request, user)
                return redirect(reverse(self.success_url))
            else:
                form = self.form_class(request.POST)
                self.context['errors'] = "Пользователь не найден"
                self.context['form'] = form
                return render(request, self.template_name, self.context)

class RegisterView(View):
    template_name = 'core/html/register.html'
    form_class = RegisterForm
    context = {}
    success_url = 'core-index'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class()
        self.context['form'] = form
        self.context['errors'] = ''
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_none(User, email=email)
            password = form.cleaned_data['password']
            double_password = form.cleaned_data['double_password']
            if user:
                self.context['errors'] = "Email занят"
                self.context['form'] = form
                return render(request, self.template_name, self.context)
            if password != double_password:
                self.context['errors'] = "Пароли не одинаковые"
                self.context['form'] = form
                return render(request, self.template_name, self.context)
            else:
                pwd = make_password(password)
                user = User.objects.create(email=email, password=pwd)
                login(request, user)
                return redirect(reverse(self.success_url), self.context)


class LogoutView(View):
    success_url = 'core-login'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse(self.success_url))

    def post(self, request, *args, **kwargs):
        pass


class ResetView(View):
    template_name = 'core/html/reset.html'
    form_class = ResetForm
    context = {'errors': ''}
    success_url = 'core-reset_success'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class()
        self.context['form'] = form
        self.context['errors'] = ''
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.success_url))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_none(User, email=email)
            if user:
                u = uuid.uuid4()
                cache.set(u, user.id, 60 * 60)
                request.session['reset'] = True
                link = "{}://{}{}".format(request.scheme, request.META.get('HTTP_HOST'),
                                          reverse('core-reset_confirm', kwargs={'user_uuid': u}))
                html_message = "<h1>Hi</h1>You need to verify your email using this link " \
                       "link <a href='{}'>here</a>. This link work only 1 hour.".format(link)
                user.email_user("Please change your password", link, html_message=html_message)
                return redirect(reverse(self.success_url))
            else:
                self.context['form'] = form
                self.context['errors'] = 'Нет такого пользователя'
                return render(request, self.template_name, self.context)


class ResetSuccessView(View):
    template_name = 'core/html/reset_success.html'
    login_url = 'core-login'
    def get(self, request, *args, **kwargs):
        if request.session.get('reset'):
            del request.session['reset']
            return render(request, self.template_name)
        else:
            return redirect(reverse(self.login_url))

    def post(self, request, *args, **kwargs):
        pass

class ResetConfirmView(View):
    form_class = PasswordResetEmailForm
    success_url = "core-index"
    template_name = 'core/html/password_reset.html'
    context = {}

    def get(self, request, user_uuid, *args, **kwargs):
        id = cache.delete(user_uuid)
        user = get_object_or_none(User, pk=id)
        if user:
            form = self.form_class()
            self.context['form'] = form
            request.session['change'] = user.id
            return render(request, self.template_name, context=self.context)
        else:
            raise Http404
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_object_or_none(User, pk=request.session.get('change'))
            if user:
                if form.cleaned_data['password'] != form.cleaned_data['double_password']:
                    self.context['form'] = form
                    self.context['errors'] = "Ваши пароли не одинаковые"
                    return render(request, self.template_name, context=self.context)
                else:
                    del request.session['change']
                    pwd = make_password(form.cleaned_data['double_password'])
                    user.password = pwd
                    user.save()
                    login(request, user)
                    return redirect(reverse(self.success_url))
            else:
                raise Http404