
# Create your views here.
# orders/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import ProductCreateForm
from .models import Product

@login_required
def index(request):
    user = request.user

    # Prevent "viewer" role creating products (optional - adjust if you want different policy)
    can_create = user.role in ("admin", "operator")

    if request.method == "POST":
        if not can_create:
            messages.error(request, "You do not have permission to create products.")
            return redirect("orders:index")

        form = ProductCreateForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # assign company and creator automatically
            product.company = user.company
            product.created_by = user
            # created_at is auto-set by model default but ensure it's set here if needed:
            # product.created_at = timezone.now()
            product.save()
            messages.success(request, f"Product '{product.name}' created.")
            return redirect("orders:index")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductCreateForm()

    # list products belonging to user's company (optionally show both active/inactive)
    products = Product.objects.filter(company=user.company).order_by("-created_at")

    context = {
        "form": form,
        "products": products,
        "can_create": can_create,
    }
    return render(request, "orders/index.html", context)
