# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from core.forms import SupportForm, ProductForm, BasketForm
from core.models import Product, BasketProduct
from core.tool import get_object_or_none
from techshop.settings import EMAIL_HOST_USER


class IndexView(View):
    template_name = "core/html/index.html"
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
    template_name = 'core/html/product.html'
    context = {}
    form_class = ProductForm
    def get(self, request, id, *args, **kwargs):
        product = get_object_or_none(Product, pk=id)
        form = self.form_class()
        if product:
            self.context['product'] = product
            self.context['form'] = form
            return render(request, self.template_name, self.context)
        else:
            raise Http404

    def post(self, request, id, *args, **kwargs):
        form = self.form_class(request.POST)
        product = get_object_or_none(Product, pk=id)
        if form.is_valid() and product:
            if request.user.is_authenticated:
                self.context['product'] = product
                self.context['form'] = form

                basket_products = request.user.basket.all()
                # increase amount
                for basket_product in basket_products:
                    if product == basket_product.product:
                        basket_product.amount += form.cleaned_data['amount']
                        basket_product.save()
                        return render(request, self.template_name, self.context)
                # create new
                BasketProduct.objects.create(user=request.user, product=product,
                                            amount=form.cleaned_data['amount'])
            return render(request, self.template_name, self.context)


class BasketView(LoginRequiredMixin, View):
    template_name = 'core/html/basket.html'
    context = {}
    form_class = BasketForm
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

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
