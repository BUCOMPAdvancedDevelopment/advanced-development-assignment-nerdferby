from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from address.models import AddressField  # django-address
from AdvancedDevelopment.firebase import FirebaseClient
from .utils import generate_id


class Product(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=128)
    desc = models.TextField(max_length=512)
    # img  # todo add through google cloud storage
    # price = models.FloatField()

    # def get_absolute_url(self):
    #     # todo issue: id is not set until after model is saved
    #     #   Reverse for 'product' with keyword arguments '{'pk': ''}' not found.
    #     #   1 pattern(s) tried: ['product/(?P<pk>[^/]+)/$']
    #     return reverse("product", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        client = FirebaseClient("products")
        id_gen = generate_id(client)
        store_data = {"id": id_gen,
                      "name": self.name,
                      "desc": self.desc}
        client.create(document=str(id_gen), data=store_data)


class Order(models.Model):
    STATUS_CHOICES = [
        ("1", "Order confirmed"),
        ("2", "Awaiting dispatch"),
        ("3", "Dispatched, awaiting courier"),
        ("4", "With courier, awaiting delivery"),
        ("5", "Out for delivery"),
        ("6", "Order delivered and fulfilled")
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = AddressField()
    status = models.CharField(default="1", max_length=1, choices=STATUS_CHOICES)
    customer = get_user_model()

    def get_absolute_url(self):
        return reverse("order", kwargs={"pk": self.pk})

