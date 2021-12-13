from django.contrib.auth import get_user_model
from django.db import models
from address.models import AddressField  # django-address


class Product(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField(max_length=500)
    # img  # todo add through google cloud storage
    price = models.FloatField()


STATUS_CHOICES = [
    ("1", "Order confirmed"),
    ("2", "Awaiting dispatch"),
    ("3", "Dispatched, awaiting courier"),
    ("4", "With courier, awaiting delivery"),
    ("5", "Out for delivery"),
    ("6", "Order delivered and fulfilled")
]


class Shipping(models.Model):
    address = AddressField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.status


class Parcel(models.Model):
    products = models.ManyToManyField(Product)
    shipping = Shipping
    customer = get_user_model()

