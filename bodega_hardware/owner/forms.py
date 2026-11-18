from django import forms

from inventory.models import Category, Product


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        Category.objects.all(), required=False, empty_label="Choose a category"
    )
    new_category = forms.CharField(required=False, max_length=100, label="Or add a new category")
    opening_stock = forms.IntegerField(min_value=0, initial=0, required=False, label="Opening stock")

    field_order = [
        "name", "sku", "category", "new_category", "price", "unit",
        "reorder_level", "opening_stock", "description", "image", "is_active",
    ]

    class Meta:
        model = Product
        fields = ("name", "sku", "price", "unit", "reorder_level", "description", "image", "is_active")
        labels = {
            "sku": "SKU",
            "price": "Price (₱)",
            "reorder_level": "Warn when stock is at or below",
            "is_active": "Show in the shop",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # stock of an existing product is changed with the + / - buttons
            self.fields.pop("opening_stock")
            self.fields["category"].initial = self.instance.category_id

    def clean(self):
        data = super().clean()
        if not data.get("category") and not (data.get("new_category") or "").strip():
            raise forms.ValidationError("Choose a category or type a new one.")
        return data

    def save(self, commit=True):
        product = super().save(commit=False)
        new_name = (self.cleaned_data.get("new_category") or "").strip()
        if new_name:
            product.category, _ = Category.objects.get_or_create(name=new_name)
        else:
            product.category = self.cleaned_data["category"]
        if commit:
            product.save()
        return product
