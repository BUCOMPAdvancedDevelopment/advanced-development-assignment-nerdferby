from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import DetailView, CreateView

from products.models import Product, Order


def home(request):
    return render(request, "products/home.html")


def product_detail_view(request, pk):
    from AdvancedDevelopment.firebase import FirebaseClient
    client = FirebaseClient("products")
    product_doc = client.get_by_id(pk)
    if product_doc is not False:
        return render(request, "products/product_detail.html", {"product": product_doc})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


# class ProductDetailView(DetailView):
#     model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "desc"]


class OrderDetailView(DetailView):
    model = Order


class OrderCreateView(CreateView):
    model = Order
    fields = ["product", "quantity", "address"]

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
