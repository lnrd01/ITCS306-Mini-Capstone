from django.contrib import messages
from django.shortcuts import redirect

CUSTOMER_ONLY = ("/cart/", "/orders/")


class KeepStaffOutOfShopMiddleware:
    """Staff manage the store in /admin/, so they can't use cart, checkout or My orders."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.is_staff and request.path.startswith(CUSTOMER_ONLY):
            messages.info(request, "Staff accounts manage the store here. Use a customer account to shop.")
            return redirect("owner_stock")
        return self.get_response(request)