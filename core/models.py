from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import ForeignKey


class User(AbstractUser):
    address = models.CharField(max_length=255)


class Basket(models.Model):
    """
    Example products {'products': [{'id', 1, 'amount': 1}, {'id', 2, 'amount': 1}]}
    Example products {'products': {'1': 1, '2': 2} } - THis is better

    """
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    total_price = models.FloatField()
    products = models.JSONField()

