from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.db.models import ForeignKey

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1000)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    # products = models.ManyToManyField(Product)

    def get_total_price(self):
        return self.product

    def __str__(self):
        return self.user.email
class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_product')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product')
    amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class Order(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    total_price = models.FloatField()
    products = models.ManyToManyField(Product)
    order_time = models.DateTimeField()
    delivery_time = models.DateTimeField()