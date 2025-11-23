from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class company(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("operator", "Operator"),
        ("viewer", "Viewer"),
    )
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default="viewer")
    company = models.ForeignKey(company, on_delete=models.PROTECT, related_name="users",blank=True, null=True)
    def __str__(self):
        return f"{self.username} ({self.role})"