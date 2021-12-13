from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from products.models import Product, Order


def home(request):
    return render(request, "products/home.html")


class ProductDetailView(DetailView):
    model = Product


class OrderDetailView(DetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["product", "quantity", "address"]

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
