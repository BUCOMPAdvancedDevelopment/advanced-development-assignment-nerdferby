from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from address.models import AddressField  # django-address


class Product(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField(max_length=512)
    # img  # todo add through google cloud storage
    price = models.FloatField()

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})


class Order(models.Model):
    STATUS_CHOICES = [
        ("1", "Order confirmed"),
        ("2", "Awaiting dispatch"),
        ("3", "Dispatched, awaiting courier"),
        ("4", "With courier, awaiting delivery"),
        ("5", "Out for delivery"),
        ("6", "Order delivered and fulfilled")
    ]

    product = Product
    quantity = models.IntegerField()
    # address = AddressField()  # todo needs default value as migrations have been made
    status = models.CharField(default="1", max_length=1, choices=STATUS_CHOICES)
    customer = get_user_model()

    def get_absolute_url(self):
        return reverse("order", kwargs={"pk": self.pk})

