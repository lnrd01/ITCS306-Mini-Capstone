from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from inventory.models import Product, StockMovement
from shop.cart import Cart

from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)
    rows = cart.rows()
    if not rows:
        messages.info(request, "Your cart is empty.")
        return redirect("cart")

    form = CheckoutForm(request.POST or None, initial={"full_name": request.user.get_full_name()})
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for row in rows:
                    product, quantity = row["product"], row["quantity"]
                    in_stock = Product.objects.with_stock().get(pk=product.pk).stock
                    if quantity > in_stock:
                        raise ValueError(f"Only {in_stock} {product.name} left in stock.")
                    OrderItem.objects.create(
                        order=order, product=product, product_name=product.name,
                        unit_price=product.price, quantity=quantity,
                    )
                    StockMovement.objects.create(
                        product=product, quantity=-quantity, reason=StockMovement.Reason.SALE,
                        note=f"Order #{order.pk}", created_by=request.user,
                    )
        except ValueError as error:  # the transaction is rolled back, so no stock is lost
            messages.error(request, str(error))
            return redirect("cart")
        cart.clear()
        messages.success(request, f"Order #{order.pk} placed. Pay on delivery.")
        return redirect("order_detail", pk=order.pk)

    return render(request, "orders/checkout.html", {
        "form": form, "rows": rows, "total": Cart.total(rows),
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
