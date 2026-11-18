# Bodega Hardware

A hardware store website with a storage (inventory) management system, built with Django.

- **Customers** can browse products, send a message through the contact form, add items to the cart, and place orders.
- **The shop owner** uses the Owner dashboard to add products, adjust stock, and manage orders.

## Requirements

Install these before running the project:

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.12 or newer | Check with `python --version` |
| Git | any recent version | Needed to clone the repository |
| Internet connection | | The page styling (Tailwind) and fonts load from a CDN |

The Python packages (Django, Pillow, and their dependencies) are listed in `requirements.txt` and installed in step 3.

## Setup

Run these commands in a terminal (Windows Command Prompt shown).

**1. Clone the repository**
```
git clone https://github.com/Lnrd01/ITCS306-Mini-Capstone.git
cd ITCS306-Mini-Capstone
```

**2. Create and activate a virtual environment**
```
python -m venv venv
venv\Scripts\activate
```
In PowerShell, run `venv\Scripts\Activate.ps1` instead. You should see `(venv)` at the start of the prompt.

**3. Install the packages**
```
pip install -r requirements.txt
```

**4. Create the database**
```
cd bodega_hardware
python manage.py migrate
```

**5. Create the owner (admin) account**
```
python manage.py createsuperuser
```
Enter a username and password. This account is the shop owner. It manages the shop and cannot place orders.

**6. Start the server**
```
python manage.py runserver
```

## Using the site

| Page | Address |
|---|---|
| Shop (landing page) | http://127.0.0.1:8000/ |
| Products | http://127.0.0.1:8000/products/ |
| Owner dashboard (owner login required) | http://127.0.0.1:8000/owner/ |
| Django admin (owner login required) | http://127.0.0.1:8000/admin/ |

1. Log in with the owner account. You land on the Owner dashboard.
2. Click **Add product** to create products. Enter an opening stock so customers can buy them.
3. In Django admin, open **Site settings** to edit the About text, address, phone number, and email shown on the landing page. Customer messages from the contact form appear under **Contact messages**.
4. Log out, then **Sign up** to create a customer account and try adding items to the cart and checking out.

Tip: use two different browsers (or a private window) to stay logged in as the owner and a customer at the same time.

## Optional: images

Put your own photos in `bodega_hardware/static/img/`:

- `hero.jpg` for the landing page banner
- `about.jpg` for the About section

Product photos are uploaded from the Add product / Edit product form and saved in `bodega_hardware/media/` (not tracked by Git).

## Project structure

```
ITCS306-Mini-Capstone/
├── requirements.txt
└── bodega_hardware/
    ├── manage.py
    ├── bodega_hardware/   settings and main URLs
    ├── pages/             landing page, About, contact form
    ├── accounts/          sign up, log in, log out
    ├── inventory/         categories, products, stock movements
    ├── shop/              product pages and cart
    ├── orders/            checkout and order history
    ├── owner/             owner dashboard (stock, orders, add/edit product)
    ├── templates/         shared page layout
    └── static/            images
```

## Troubleshooting

- **`No module named 'django'`**: the virtual environment is not active. Run `venv\Scripts\activate` again from the repository folder.
- **Page looks unstyled**: check your internet connection, since the styling loads from a CDN.
- **`pip` SSL certificate errors**: run `pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org`.
- **The database is not shared**: `db.sqlite3` is not committed, so every teammate runs steps 4 and 5 and adds their own test products.
