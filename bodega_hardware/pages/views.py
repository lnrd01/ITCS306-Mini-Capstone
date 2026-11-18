from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import SiteSettings


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent. We'll get back to you soon.")
            return redirect("/#contact")
    else:
        form = ContactForm()
    return render(request, "pages/home.html", {"form": form, "site": SiteSettings.load()})
