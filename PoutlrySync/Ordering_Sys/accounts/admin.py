from django.contrib import admin

# Register your models here.
from .models import  CustomUser, company
from django.contrib.auth.admin import UserAdmin

admin.site.register(company)
admin.site.register(CustomUser, UserAdmin)
