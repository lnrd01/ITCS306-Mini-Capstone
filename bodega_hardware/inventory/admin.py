from django.contrib import admin

from .models import Category, Product, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "stock_display", "low_stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "sku")

    def get_queryset(self, request):
        return super().get_queryset(request).with_stock()

    @admin.display(description="Stock")
    def stock_display(self, obj):
        return f"{obj.stock} {obj.unit}"

    @admin.display(boolean=True, description="Low stock")
    def low_stock(self, obj):
        return obj.is_low_stock


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "reason", "note", "created_by", "created_at")
    list_filter = ("reason", "created_at")
    search_fields = ("product__name", "product__sku", "note")
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
