from django.contrib import admin

# Register your models here.
import csv
from django.http import HttpResponse
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "price", "stock", "is_active")
    list_filter = ("company", "is_active")
    actions = ["mark_selected_inactive"]

    def mark_selected_inactive(self, request, queryset):
        updated = queryset.update(is_active=False, is_deleted=True)
        self.message_user(request, f"{updated} products marked as inactive.")
    mark_selected_inactive.short_description = "Mark selected products as inactive"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "company", "quantity", "status", "created_by", "created_at")
    list_filter = ("status", "company")
    actions = ["export_orders_csv"]

    def export_orders_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Product", "Quantity", "Status", "Created By", "Created At"])

        for order in queryset:
            writer.writerow([
                order.id,
                order.product.name,
                order.quantity,
                order.status,
                order.created_by.username if order.created_by else "",
                order.created_at
            ])

        return response

    export_orders_csv.short_description = "Export selected orders to CSV"