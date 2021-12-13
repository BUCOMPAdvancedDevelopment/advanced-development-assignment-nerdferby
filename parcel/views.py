from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from parcel.models import Product, Parcel


def home(request):
    return render(request, "parcel/home.html")


class ProductDetailView(DetailView):
    model = Product


class ParcelDetailView(DetailView):
    model = Parcel


class ParcelCreateView(CreateView):
    model = Parcel
    fields = ["products", "shipping"]
