# orders/forms.py
from django import forms
from .models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("company", "created_by", "created_at", "last_updated_at", "is_deleted")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Product name", "class": "form-control"}),
            "price": forms.NumberInput(attrs={"step": "0.01", "class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
