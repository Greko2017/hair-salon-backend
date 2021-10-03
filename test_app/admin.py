from django.contrib import admin

# Register your models here.
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["firstname","lastname","email","gender","phone_number"]

    search_fields = ['firstname',]

class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ["get_customer_field","account_number","amount","status"]

    search_fields = ['account_number',]
    
    def get_customer_field(self, obj):
        queryset = Customer.objects.get(account_details_id=obj.id)
        firstname = queryset.firstname
        return firstname
    get_customer_field.short_description = 'customer' 

admin.site.register(Customer, CustomerAdmin)
admin.site.register(AccountDetails, AccountDetailsAdmin)