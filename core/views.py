# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from core.forms import SupportForm, ProductForm, BasketForm
from core.models import Product, BasketProduct, Category
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
    template_name = 'core/html/category.html'
    form_class = SupportForm
    context = {'errors': ''}
    # success_url = 'core-index'
    def get(self, request, id, *args, **kwargs):
        category = get_object_or_none(Category, pk=id)
        self.context['category'] = category
        all_products = Product.objects.filter(categories=category).order_by('-id')
        current_page = Paginator(all_products, 5)
        page = request.GET.get('page')
        try:
            # Если существует, то выбираем эту страницу
            self.context['products'] = current_page.page(page)
        except PageNotAnInteger:
            # Если None, то выбираем первую страницу
            self.context['products'] = current_page.page(1)
        except EmptyPage:
            # Если вышли за последнюю страницу, то возвращаем последнюю
            self.context['products'] = current_page.page(current_page.num_pages)

        return render(request, self.template_name, self.context)

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
