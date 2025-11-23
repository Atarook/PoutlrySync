# orders/urls.py
from django.urls import path , include
from . import views
from django.contrib import admin

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),

]
