from django.contrib import admin

from .models import BankAccount


@admin.register(BankAccount)
class CheckingAdmin(admin.ModelAdmin):
    list_display = ['user', 'accounttype', 'current_asset']

