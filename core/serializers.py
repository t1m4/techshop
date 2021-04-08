from django.db import IntegrityError
from rest_framework import serializers

from core.models import OrderProduct, Product
from core.tool import get_object_or_none


class ProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)

    def create(self, validated_data, *args, **kwargs):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        product = get_object_or_none(Product, pk=validated_data.get('id'))
        amount = validated_data.get('amount')
        order = validated_data.get('order')
        if product:
            return OrderProduct.objects.create(order=order, product=product, amount=amount)
        else:
            raise IntegrityError