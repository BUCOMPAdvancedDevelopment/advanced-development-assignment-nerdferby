from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import CreateView

import users.views
from AdvancedDevelopment.firebase import FirebaseClient
from products.models import Product
from .utils import generate_id

client_products = FirebaseClient("products")

ORDER_STATUS_TEXT = [
    ("1", "Order pending"),
    ("2", "Order confirmed, awaiting dispatch"),
    ("3", "Dispatched, awaiting courier"),
    ("4", "With courier, awaiting delivery"),
    ("5", "Out for delivery"),
    ("6", "Order delivered and fulfilled")
]


def home(request):
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)
    logged_in = False
    if get_user:
        logged_in = True
    all_products = client_products.all()
    return render(request, "products/home.html", {"products": all_products,
                                                  "logged_in": logged_in})


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "desc"]


def product_detail_view(request, pk):
    product_doc = client_products.get_by_id(pk)

    if product_doc is not False:
        return render(request, "products/product_detail.html", {"product": product_doc})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def progress_order(request, pk):
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)
    client_orders = FirebaseClient("orders")
    order = client_orders.get_by_id(pk)
    if not get_user:
        return redirect(users.views.login)
    elif get_user["username"] != "admin":
        return redirect(users.views.login)
    else:
        status = int(order["status"]) + 1
        new_data = get_user
        new_data["status"] = status
        client_orders.update(pk, new_data)
        messages.success(request, "Order progressed to: " + str(status))
        return redirect(my_orders)


def my_orders(request):
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)
    if not get_user:
        return redirect(users.views.login)
    else:
        all_my_orders = FirebaseClient("orders").filter("uid", "==", get_user["username"])
        all_products = FirebaseClient("products").all()
        admin = False
        if get_user["username"] == "admin":
            admin = True
        for order in all_my_orders:
            try:
                order["status"] = ORDER_STATUS_TEXT[order["status"]][1]
            except IndexError:
                order["status"] = ORDER_STATUS_TEXT[5][1]
        context = {"my_orders": all_my_orders,
                   "products": all_products,
                   "admin": admin}
        return render(request, "products/my_orders.html", context)


def order_detail_view(request, pk):
    order = FirebaseClient("orders").get_by_id(pk)
    return render(request, "products/order_detail.html")


def cancel_order(request, pk):
    client = FirebaseClient("orders")
    order = client.get_by_id(pk)
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)
    if not get_user:
        return redirect(users.views.login)
    else:
        if order["uid"] != get_user["username"]:  # checks if order matches to logged-in user
            return redirect(home)
        else:  # delete order
            client.delete_by_id(pk)
            messages.success(request, "Order successfully cancelled")
    return redirect(my_orders)


def order(request, pk):
    try:
        session = request.session["login"]
        get_user = FirebaseClient("users").get_by_id(session)

        if get_user:
            product_doc = client_products.get_by_id(pk)
            if not product_doc:
                return redirect(home)
            client_orders = FirebaseClient("orders")
            order_id = generate_id(client_orders)
            address = f"{get_user['address1']} {get_user['address2']} {get_user['address3']} {get_user['post_code']}"
            data = {"uid": get_user["id"], "id": order_id,
                    "status": 0, "address": address,
                    "product_name": client_products.get_by_id(pk)["name"]}
            client_orders.create(document=order_id, data=data)
            messages.success(request, f"{product_doc['name']} successfully ordered!")
            return redirect(my_orders)
        else:
            session = request.session["login"]
            raise Exception("User not found")
    except KeyError:
        return redirect(users.views.login)  # redirect to login page if not logged in


# class ProductDetailView(DetailView):
#     model = Product
# class OrderDetailView(DetailView):
#     model = Order
#
#
# class OrderCreateView(CreateView):
#     model = Order
#     fields = ["product", "quantity", "address"]
#
#     def form_valid(self, form):
#         form.instance.customer = self.request.user
#         return super().form_valid(form)
