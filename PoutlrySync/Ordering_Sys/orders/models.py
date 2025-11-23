from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import company

class Product(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_products")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # for soft-delete

    def soft_delete(self):
        self.is_active = False
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    company = models.ForeignKey(company, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="orders")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    shipped_at = models.DateTimeField(null=True, blank=True)

    def set_status_success(self):
        """Mark order as success and set shipped_at timestamp."""
        self.status = "success"
        self.shipped_at = timezone.now()
        self.save()
        self.log_confirmation_email()

    def log_confirmation_email(self):
        with open("order_confirmation.log", "a") as f:
            f.write(
                f"[{timezone.now()}] Order {self.id} SUCCESS "
                f"User: {self.created_by} "
                f"Product: {self.product.name} "
                f"Quantity: {self.quantity}\n"
            )


    def __str__(self):
        return f"Order {self.id} - {self.product.name} x {self.quantity}"
