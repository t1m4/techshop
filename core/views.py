# Create your views here.
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.db.models import Sum, F, FloatField, Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.forms import SupportForm, ProductForm, BasketForm, SearchForm, SortForm, AccountForm
from core.models import Product, BasketProduct, Category, Order
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
            except Exception as e:
                print(e)
                raise Http404
class CategoriesView(View):
    template_name = 'core/html/categories.html'
    context = {'errors': ''}

    def get(self, request, *args, **kwargs):
        category = get_object_or_none(Category, pk=1)
        self.context['category'] = category
        all_categories = Category.objects.all().order_by('-id')
        current_page = Paginator(all_categories, 5)
        page = request.GET.get('page')
        try:
            # Если существует, то выбираем эту страницу
            self.context['categories'] = current_page.page(page)
        except PageNotAnInteger:
            # Если None, то выбираем первую страницу
            self.context['categories'] = current_page.page(1)
        except EmptyPage:
            # Если вышли за последнюю страницу, то возвращаем последнюю
            self.context['categories'] = current_page.page(current_page.num_pages)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass

class CategoryView(View):
    template_name = 'core/html/category.html'
    context = {'errors': ''}
    form_class = SortForm
    # success_url = 'core-index'
    def get(self, request, id, *args, **kwargs):
        form = self.form_class()
        category = get_object_or_none(Category, pk=id)
        self.context['category'] = category
        self.context['form'] = form
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

    def post(self, request, id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            category = get_object_or_none(Category, pk=id)
            self.context['category'] = category
            self.context['form'] = form
            all_products = Product.objects.filter(categories=category).order_by(choice)
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
            self.context['category'] = product.categories.all()[0]
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
    template_name = 'core/html/account.html'
    context = {}
    form_class = AccountForm
    success_url = 'core-account'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form'] = form
        self.context['range'] = range(2)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            for k, v in form.cleaned_data.items():
                setattr(request.user, k, v)
            request.user.save()
            self.context['form'] = form
            self.context['range'] = range(2)
            return redirect(reverse(self.success_url))
        else:
            raise Http404

class OrdersView(View):
    template_name = 'core/html/orders.html'
    context = {}

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user).order_by('-id')
        self.context['orders'] = orders
        current_page = Paginator(orders, 5)
        page = request.GET.get('page')
        try:
            # Если существует, то выбираем эту страницу
            self.context['orders'] = current_page.page(page)
        except PageNotAnInteger:
            # Если None, то выбираем первую страницу
            self.context['orders'] = current_page.page(1)
        except EmptyPage:
            # Если вышли за последнюю страницу, то возвращаем последнюю
            self.context['orders'] = current_page.page(current_page.num_pages)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass


class OrderView(LoginRequiredMixin, View):
    template_name = 'core/html/order.html'
    context = {}
    form_class = BasketForm
    success_url = 'core-orders-view'

    def get(self, request, id, *args, **kwargs):
        order = get_object_or_none(Order, pk=id)
        if order:
            if order.user == request.user:
                products = order.order_products.all().annotate(
                    total=Sum(F('product__price') * F('amount'), output_field=FloatField()))
                self.context['products'] = products
                total_sum = order.order_products.all().aggregate(
                    total=Sum(F('product__price') * F('amount'), output_field=FloatField()))
                self.context['total_sum'] = total_sum.get('total')
                self.context['products'] = products
                self.context['order_id'] = order.id if order.status != 'cancel' else None
                print(self.context['order_id'], order.status)
                return render(request, self.template_name, self.context)
        raise Http404()
    def post(self, request, id, *args, **kwargs):
        order = get_object_or_none(Order, pk=id)
        if order.user == request.user:
            order.status = 'cancel'
            order.save()
        return redirect(reverse(self.success_url))

@method_decorator(csrf_exempt, name='dispatch')
class SearchView(View):
    template_name = 'core/html/search.html'
    context = {'errors': ''}
    success_url = 'core-index'
    form_class = SearchForm
    # success_url = 'core-index'
    def get(self, request, *args, **kwargs):
        search = request.session.get('search')
        # search = request.GET.get('search')
        if search:
            # all_products = Product.objects.filter(Q(name__icontains=search)).order_by('-id')
            all_categories = Category.objects.filter(name__icontains=search).order_by('-id')
            all_products = Product.objects.filter(Q(name__icontains=search) | Q(categories__in=all_categories)).order_by('-id')
            current_page = Paginator(all_products, 10)
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
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['search'] = form.cleaned_data['search']
            return HttpResponse('ok', status=301)
            # return redirect(reverse(self.success_url))
        else:
            return HttpResponse('ok', status=404)
