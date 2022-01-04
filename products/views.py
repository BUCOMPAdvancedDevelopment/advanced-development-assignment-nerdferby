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
    """Renders homepage. Context: all products (obj) and if user logged-in (bool)"""
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)
    logged_in = False
    if get_user:  # if user is logged in
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
    """
    Progresses an order's status, e.g. dispatch to delivery
    Requires an admin to progress
    :param request
    :param pk: Order ID
    :return: Redirects to login page if not admin, to My Orders if successful
    """
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
    """
    My Orders page for logged in user, containing all pending orders and their status
    :param request
    :return: Redirects to login if user not logged in, to my orders if logged in
    """
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)
    if not get_user:
        return redirect(users.views.login)
    else:
        all_my_orders = FirebaseClient("orders").filter("uid", "==", get_user["username"])  # find all orders for user
        all_products = FirebaseClient("products").all()
        admin = False
        if get_user["username"] == "admin":
            admin = True
        for order in all_my_orders:
            try:
                order["status"] = ORDER_STATUS_TEXT[order["status"]][1]  # change status enum to text
            except IndexError:
                order["status"] = ORDER_STATUS_TEXT[5][1]
        context = {"my_orders": all_my_orders,
                   "products": all_products,
                   "admin": admin}
        return render(request, "products/my_orders.html", context)


# def order_detail_view(request, pk):
#     order = FirebaseClient("orders").get_by_id(pk)
#     return render(request, "products/order_detail.html")


def cancel_order(request, pk):
    """
    Cancels an order and removes it from the db, requires logged-in user
    :param request:
    :param pk: Order ID
    :return: Redirects to home if not logged-in, to my orders if logged in
    """
    client = FirebaseClient("orders")
    order = client.get_by_id(pk)
    session = request.session["login"]
    get_user = FirebaseClient("users").get_by_id(session)

    if not get_user:  # if not logged-in, redirect to login
        return redirect(users.views.login)
    else:
        if order["uid"] != get_user["username"]:  # checks if order matches to logged-in user
            return redirect(home)
        else:  # delete order
            client.delete_by_id(pk)  # delete order from db
            messages.success(request, "Order successfully cancelled")
    return redirect(my_orders)


def order(request, pk):
    """
    Place order, add to db, requires user logged-in
    :param request:
    :param pk: Product ID
    :return:
    """
    try:
        session = request.session["login"]
        get_user = FirebaseClient("users").get_by_id(session)

        if get_user:  # if user is logged-in
            product_doc = client_products.get_by_id(pk)  # product
            if not product_doc:  # if product doesn't exist, redirect to home
                return redirect(home)
            client_orders = FirebaseClient("orders")
            gen_id = generate_id(client_orders)  # generate order id
            address = f"{get_user['address1']} {get_user['address2']} {get_user['address3']} {get_user['post_code']}"
            data = {"uid": get_user["id"], "id": gen_id,
                    "status": 0, "address": address,
                    "product_name": client_products.get_by_id(pk)["name"]}
            client_orders.create(document=gen_id, data=data)  # create order in db
            messages.success(request, f"{product_doc['name']} successfully ordered!")
            return redirect(my_orders)
        else:
            session = request.session["login"]
            raise Exception("User not found")
    except KeyError:
        return redirect(users.views.login)  # redirect to login page if not logged in
