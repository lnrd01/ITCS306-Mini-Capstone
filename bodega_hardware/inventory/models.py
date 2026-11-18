from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def with_stock(self):
        """Adds stock_total (sum of all stock movements) in a single query."""
        return self.annotate(stock_total=Coalesce(Sum("movements__quantity"), 0))


class Product(models.Model):
    class Unit(models.TextChoices):
        PIECE = "pc", "Piece"
        BOX = "box", "Box"
        METER = "m", "Meter"
        KILOGRAM = "kg", "Kilogram"
        LITER = "l", "Liter"

    name = models.CharField(max_length=200)
    sku = models.CharField("SKU", max_length=50, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.PIECE)
    reorder_level = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def stock(self):
        if "stock_total" in self.__dict__:  # already annotated
            return self.stock_total
        return self.movements.aggregate(total=Sum("quantity"))["total"] or 0

    @property
    def is_low_stock(self):
        return self.stock <= self.reorder_level


class StockMovement(models.Model):
    class Reason(models.TextChoices):
        RESTOCK = "restock", "Restock"
        SALE = "sale", "Sale"
        RETURN = "return", "Customer return"
        DAMAGED = "damaged", "Damaged / lost"
        ADJUSTMENT = "adjustment", "Adjustment"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="movements")
    quantity = models.IntegerField(help_text="Positive adds stock, negative removes stock")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.sku}: {self.quantity:+d} ({self.reason})"
