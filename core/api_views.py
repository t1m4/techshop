import datetime

from django.db import IntegrityError
from django.db.models import Sum, F, FloatField
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from core.models import Product, BasketProduct, Order
from core.serializers import ProductsSerializer
from core.tool import get_object_or_none


class DeleteProductView(View):
    def get(self, request, id, *args, **kwargs):
        # Берем продукт
        product = get_object_or_none(Product, pk=id)
        # Проверяем что пользователь авторизован
        if request.user.is_authenticated:
            # Берем все продукты из корзины
            basket_products = request.user.basket.all()
            for basket_product in basket_products:
                # Если продукт есть в корзине удаляем его
                if product == basket_product.product:
                    basket_product.delete()
                    return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'})

class BasketProductView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            products = BasketProduct.objects.filter(user=request.user)
            response = {'status': 'ok', 'products': []}
            for product in products:
                response['products'].append({
                    'id': product.product.id,
                    'amount': product.amount,
                    'name': product.product.name,
                    'price': product.product.price,
                })
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error'})

@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    context = {'status': 'error'}
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = JSONParser().parse(request)
            if data.get('products'):
                serializer = ProductsSerializer(data=data['products'], many=True)
                if serializer.is_valid():
                    order = Order.objects.create(
                        user=request.user,
                        order_time=datetime.datetime.now(),
                        delivery_time=datetime.datetime.now() + datetime.timedelta(1),
                    )
                    try:
                        serializer.save(order=order)
                        total_price = order.order_products.all().aggregate(
                            total=Sum(F('product__price') * F('amount'), output_field=FloatField()))
                        order.total_price = total_price.get('total')
                        order.save(update_fields=['total_price'])
                        self.context['status'] = 'ok'
                    except IntegrityError:
                        self.context['status'] = 'not_valid'

                else:
                    self.context['status'] = 'not_valid'
        return JsonResponse(self.context)