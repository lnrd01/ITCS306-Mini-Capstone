from inventory.models import Product


class Cart:
    """Session-based cart: {product_id: quantity}."""

    def __init__(self, request):
        self.session = request.session
        self.data = dict(self.session.get("cart", {}))

    def _save(self):
        self.session["cart"] = self.data

    def add(self, product_id, quantity):
        key = str(product_id)
        self.data[key] = self.data.get(key, 0) + quantity
        self._save()

    def set(self, product_id, quantity):
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.data[str(product_id)] = quantity
            self._save()

    def remove(self, product_id):
        self.data.pop(str(product_id), None)
        self._save()

    def clear(self):
        self.data = {}
        self._save()

    def quantity_of(self, product_id):
        return self.data.get(str(product_id), 0)

    def __len__(self):
        return sum(self.data.values())

    def rows(self):
        products = Product.objects.with_stock().filter(pk__in=self.data.keys(), is_active=True)
        return [
            {"product": p, "quantity": self.data[str(p.pk)], "subtotal": p.price * self.data[str(p.pk)]}
            for p in products
        ]

    @staticmethod
    def total(rows):
        return sum(r["subtotal"] for r in rows)
