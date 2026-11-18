from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def after_login(request):
    """Staff go to the admin panel, customers go to the shop."""
    return redirect("owner_stock" if request.user.is_staff else "home")