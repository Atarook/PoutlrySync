from django.urls import path
from .views import (
    ProductListView,
    ProductDeleteView,
    OrderCreateView,
    OrderExportView
)

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/delete/", ProductDeleteView.as_view()),
    path("orders/", OrderCreateView.as_view()),
    path("orders/export/", OrderExportView.as_view()),
]
