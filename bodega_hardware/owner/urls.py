from django.urls import path

from . import views

urlpatterns = [
    path("", views.stock, name="owner_stock"),
    path("orders/", views.orders, name="owner_orders"),
    path("products/add/", views.product_add, name="owner_product_add"),
    path("products/<int:pk>/edit/", views.product_edit, name="owner_product_edit"),
    path("products/<int:pk>/adjust/", views.stock_adjust, name="owner_stock_adjust"),
    path("orders/<int:pk>/status/", views.order_status, name="owner_order_status"),
    path("orders/<int:pk>/cancel/", views.order_cancel, name="owner_order_cancel"),
]
