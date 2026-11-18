from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from inventory.models import Category, Product

from .cart import Cart


def product_list(request):
    products = Product.objects.with_stock().filter(is_active=True).select_related("category")
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    if q:
        products = products.filter(Q(name__icontains=q) | Q(sku__icontains=q))
    if category.isdigit():
        products = products.filter(category_id=category)
    return render(request, "shop/product_list.html", {
        "products": products,
        "categories": Category.objects.all(),
        "q": q,
        "category": category,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.with_stock(), pk=pk, is_active=True)
    return render(request, "shop/product_detail.html", {"product": product})


def cart_detail(request):
    rows = Cart(request).rows()
    return render(request, "shop/cart.html", {"rows": rows, "total": Cart.total(rows)})


def _quantity(request):
    try:
        return int(request.POST.get("quantity", 1))
    except ValueError:
        return 1


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product.objects.with_stock(), pk=pk, is_active=True)
    cart = Cart(request)
    quantity = max(_quantity(request), 1)
    available = product.stock - cart.quantity_of(pk)
    if quantity > available:
        quantity = max(available, 0)
        messages.warning(request, f"Only {product.stock} {product.name} in stock.")
    if quantity:
        cart.add(pk, quantity)
        messages.success(request, f"Added {quantity} x {product.name} to your cart.")
    return redirect("cart")


@require_POST
def cart_update(request, pk):
    product = get_object_or_404(Product.objects.with_stock(), pk=pk, is_active=True)
    quantity = _quantity(request)
    if quantity > product.stock:
        quantity = product.stock
        messages.warning(request, f"Only {product.stock} {product.name} in stock.")
    Cart(request).set(pk, quantity)
    return redirect("cart")


@require_POST
def cart_remove(request, pk):
    Cart(request).remove(pk)
    return redirect("cart")
