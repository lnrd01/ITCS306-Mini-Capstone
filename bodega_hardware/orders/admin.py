from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("product", "product_name", "unit_price", "quantity")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "status", "total_display", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "user__username", "phone")
    inlines = [OrderItemInline]
    actions = ["cancel_orders"]

    @admin.display(description="Total")
    def total_display(self, obj):
        return f"₱{obj.total:,.2f}"

    @admin.action(description="Cancel selected orders and return stock")
    def cancel_orders(self, request, queryset):
        count = 0
        for order in queryset:
            if order.status != Order.Status.CANCELLED:
                order.cancel()
                count += 1
        self.message_user(request, f"{count} order(s) cancelled and stock returned.")
