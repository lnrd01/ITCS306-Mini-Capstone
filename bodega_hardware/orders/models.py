from django.conf import settings
from django.db import models, transaction

from inventory.models import Product, StockMovement


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        PACKED = "packed", "Packed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def cancel(self):
        """Cancel the order and put its items back into stock."""
        if self.status == self.Status.CANCELLED:
            return
        with transaction.atomic():
            for item in self.items.all():
                StockMovement.objects.create(
                    product=item.product,
                    quantity=item.quantity,
                    reason=StockMovement.Reason.ADJUSTMENT,
                    note=f"Order #{self.pk} cancelled",
                )
            self.status = self.Status.CANCELLED
            self.save(update_fields=["status"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)  # kept in case the product is renamed later
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
