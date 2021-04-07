from django.http import HttpResponse, JsonResponse
from django.views import View

from core.models import Product, BasketProduct
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
