from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from inventory.models import Product, StockMovement
from orders.models import Order

from .forms import ProductForm
from .permissions import staff_required

TO_FULFIL = [Order.Status.PENDING, Order.Status.PAID, Order.Status.PACKED]


def _summary(products):
    return {
        "product_count": len(products),
        "low_count": sum(1 for p in products if p.is_low_stock),
        "to_fulfil": Order.objects.filter(status__in=TO_FULFIL).count(),
    }


@staff_required
def stock(request):
    products = list(Product.objects.with_stock().select_related("category"))
    return render(request, "owner/stock.html", {"products": products, "tab": "stock", **_summary(products)})


@staff_required
def orders(request):
    products = list(Product.objects.with_stock())
    return render(request, "owner/orders.html", {
        "orders": Order.objects.select_related("user").prefetch_related("items"),
        "statuses": [(v, label) for v, label in Order.Status.choices if v != Order.Status.CANCELLED],
        "tab": "orders",
        **_summary(products),
    })


@staff_required
def product_add(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        opening = form.cleaned_data.get("opening_stock") or 0
        if opening:
            StockMovement.objects.create(
                product=product, quantity=opening, reason=StockMovement.Reason.RESTOCK,
                note="Opening stock", created_by=request.user,
            )
        messages.success(request, f"{product.name} added to the shop.")
        return redirect("owner_stock")
    return render(request, "owner/product_form.html", {"form": form, "title": "Add product"})


@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{product.name} updated.")
        return redirect("owner_stock")
    return render(request, "owner/product_form.html", {"form": form, "title": f"Edit {product.name}"})


@staff_required
@require_POST
def stock_adjust(request, pk):
    product = get_object_or_404(Product.objects.with_stock(), pk=pk)
    delta = 1 if request.POST.get("delta") == "1" else -1
    if delta < 0 and product.stock <= 0:
        messages.error(request, f"{product.name} is already at 0.")
    else:
        StockMovement.objects.create(
            product=product, quantity=delta,
            reason=StockMovement.Reason.RESTOCK if delta > 0 else StockMovement.Reason.ADJUSTMENT,
            note="Quick adjust from the owner dashboard", created_by=request.user,
        )
    return redirect(f"{reverse('owner_stock')}#p{pk}")


@staff_required
@require_POST
def order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    status = request.POST.get("status")
    allowed = {v for v, _ in Order.Status.choices} - {Order.Status.CANCELLED.value}
    if order.status == Order.Status.CANCELLED:
        messages.error(request, "Cancelled orders can't be changed.")
    elif status in allowed:
        order.status = status
        order.save(update_fields=["status"])
        messages.success(request, f"Order #{order.pk} is now {order.get_status_display().lower()}.")
    return redirect("owner_orders")


@staff_required
@require_POST
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == Order.Status.CANCELLED:
        messages.error(request, f"Order #{order.pk} is already cancelled.")
    else:
        order.cancel()
        messages.success(request, f"Order #{order.pk} cancelled and its items are back in stock.")
    return redirect("owner_orders")
