"""AdvancedDevelopment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from products import views as product_views
from users import views as user_views

urlpatterns = [
    path("", product_views.home, name="home"),
    # path("", user_views.register, name="home"),
    path("admin/", admin.site.urls),
    path("product/new/", product_views.ProductCreateView.as_view(), name="product-create"),
    path("product/<str:pk>/", product_views.product_detail_view, name="product"),
    path("order/<str:pk>/", product_views.order, name="order"),
    path("my-orders/", product_views.my_orders, name="my-orders"),
    path("cancel-order/<str:pk>/", product_views.cancel_order, name="cancel-order"),
    path("progress-order/<str:pk>/", product_views.progress_order, name="progress-order"),
    # path("order/new/", product_views.OrderCreateView.as_view(), name="order-create"),
    path("register/", user_views.register, name="register"),
    # path("profile/deactivate", DeactivateUser.as_view(), name="delete-profile"),
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(template_name="users/login.html"),
    #     name="login",
    # ),
    path(
        "login/",
        user_views.login,
        name="login",
    ),
    path(
        "logout/",
        user_views.logout,
        name="logout",
    ),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url="/"
        ),
        name="password_change"
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    )
]
