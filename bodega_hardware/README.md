# Bodega Hardware: app code

## 1. Copy the files
Copy everything inside this zip's `bodega_hardware/` folder into your project folder
(the one that contains `manage.py`). Say yes to overwriting `bodega_hardware/urls.py`
and, if you already made it, the `inventory` app files.

Result:
    ITCS306-Mini-Capstone/bodega_hardware/
        manage.py
        bodega_hardware/   (settings.py, urls.py)
        pages/  accounts/  inventory/  shop/  orders/
        templates/  static/

## 2. Paste this at the very bottom of bodega_hardware/bodega_hardware/settings.py
If you already added 'inventory' to INSTALLED_APPS, you can leave it. The line below skips duplicates.

    INSTALLED_APPS += [a for a in ["pages", "accounts", "inventory", "shop", "orders"] if a not in INSTALLED_APPS]

    TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
    TEMPLATES[0]["OPTIONS"]["context_processors"].append("shop.context_processors.cart_count")

    STATICFILES_DIRS = [BASE_DIR / "static"]
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

    LOGIN_URL = "login"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "/"

## 3. Install, migrate, run (venv active, inside the folder with manage.py)
    pip install Pillow
    pip freeze > ../requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Add `media/` to your .gitignore (uploaded product photos).

## 4. Try it
1. http://127.0.0.1:8000/admin : add a Category, a Product (with a photo), then a Stock Movement of +50 (Restock).
2. Admin > Site settings: edit the About text, address, phone and email.
3. http://127.0.0.1:8000/ : landing page. Send a message through the contact form, then see it in Admin > Contact messages.
4. Sign up, add a product to the cart, check out. Stock drops by the quantity (Admin > Stock movements shows "Order #1").
5. Admin > Orders: select an order, choose "Cancel selected orders and return stock". The stock comes back.

## 5. Images from your Figma design
Export the hero photo as static/img/hero.jpg and the About photo as static/img/about.jpg.

## Notes
- Tailwind loads from a CDN, which is fine for development. Switch to a proper build before deployment.
- Checkout is pay on delivery for now. A payment gateway can be added later in the orders app.
- To change an order's status (Paid, Packed, Shipped...), edit it in the admin. Use the Cancel action (not the status dropdown) to cancel, so stock is returned.
