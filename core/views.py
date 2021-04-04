# Create your views here.
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from core.forms import SupportForm
from techshop.settings import EMAIL_HOST_USER


class IndexView(View):
    template_name = "base.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass


class SupportView(View):
    template_name = 'core/html/support.html'
    form_class = SupportForm
    context = {'errors': ''}
    success_url = 'core-index'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form'] = form
        self.context['errors'] = ''
        self.context['range'] = range(3)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                html_message = "I need some support, please asnwer me to {}, my message  {}".format(
                    form.cleaned_data['email'],
                    form.cleaned_data['message']
                )
                send_mail("Support", html_message,
                          EMAIL_HOST_USER, ['731ruslan00@mail.ru'])
                return redirect(reverse(self.success_url))
            except:
                raise Http404
class CategoriesView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class ProductView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class BasketView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class AccountView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class OrdersView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class OrderView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
