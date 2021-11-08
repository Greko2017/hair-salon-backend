from django.contrib import admin

# Register your models here.
from .models import *
from datetime import datetime

# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'name',
#     ]

#     search_fields = ['name',]

# class SalaryAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'percentage','income','is_percentage'
#     ]

#     search_fields = ['percentage','income',]

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'firstname','lastname','gender','phone_number'
#     ]

#     search_fields = ['id', 'firstname','lastname','gender','phone_number']

# class InlineServiceLine(admin.TabularInline):
#     model = ServiceLine
#     extra = 1
#     max_num= 3

# class ServiceAdmin(admin.ModelAdmin):
#     inlines =[InlineServiceLine]
#     list_display_links = ["name"]
#     list_display = [
#         'id','name', 'employee_id','created', 'total_amount_paid', 
#     ]
#     # exclude = ['name',]
#     ordering = ['-employee_id',]
#     search_fields = ['employee_id',]

#     search_fields = ['id', 'name','created']

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             # Only set added_by during the first save.
#             val = Service.objects.count()
            
#             obj.name = f'SERVICE_{datetime.now().strftime("%Y%m%d%H%M%S")}'
#         if obj.created_by is None:
#             obj.created_by = request.user
#             obj.save()
#         else:
#             obj.save()
        
#         super().save_model(request, obj, form, change)

# class CityAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'name',
#     ]

#     search_fields = ['id', 'name',]

# class StreetAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'name',
#     ]

#     search_fields = ['id', 'name',]

# class LocationAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'region', 'city_id', 'street_id',
#     ]

#     search_fields = ['id', 'region',]

# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'user', 'gender', 'phone_number', 'hired_date', 'location_id', 'salary_id',
#     ]

#     search_fields = ['id',]

# # class CategoryAdmin(admin.ModelAdmin):
# #     list_display = [
# #         'id', 'name', 'description',
# #     ]

# #     search_fields = ['id', 'name',]

# class ProductAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'name', 'description','quantity', 'cost_price', 'selling_price',# 'category_id'
#     ]

#     search_fields = ['id', 'name',]

# class SupplierAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'name', 'company_name','location_id', 'phone_number', 'email'
#     ]

#     search_fields = ['id', 'name','company_name']
# class ServiceLookupAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'name', 
#     ]

#     search_fields = ['id', 'name',]
# class ServiceLineAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 'parent_id', 'lookup','is_credit', 'customer_id', 'amount_paid','details', 'payment_method', 'created',
#     ]

#     search_fields = ['id', 'parent_id', 'lookup']
# class SaleAdmin(admin.ModelAdmin):
#   list_display = [
#     'id', 'name', 'customer_id', 'created_at'
#   ]

# class SaleLineAdmin(admin.ModelAdmin):
#   list_display = [
#     'id', 'parent_id', 'product_id', 'product_quantity','is_credit', 'amount_paid', 'payment_method','details', 'created_at'
#   ]

# class InlinePayrollOtherPay(admin.TabularInline):
#     model = PayrollOtherPay
#     extra = 1
#     max_num= 3


# class InlinePayrollDeduction(admin.TabularInline):
#     model = PayrollDeduction
#     extra = 1
#     max_num= 3


# class PayrollAdmin(admin.ModelAdmin):
#     inlines = [InlinePayrollOtherPay, InlinePayrollDeduction]
#     list_display_links =['name']
#     list_display = [
#         'id', 'name','employee', 'date_from', 'date_to','worked_value', 'computed_salary', 'net_salary', 'created_at', 'status'
#     ]

#     search_fields = ['name',]

# class PayrollOtherPayAdmin(admin.ModelAdmin):
#     list_display = ['id', 'parent', 'name','amount', 'description', 'created_at' ]
#     list_display_links =['parent']
    
# class InventoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'product','modified_at', 'created_at', 'status']
#     list_display_links =['name']

# admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Salary, SalaryAdmin)
# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Service, ServiceAdmin)
# admin.site.register(City, CityAdmin)
# admin.site.register(Street, StreetAdmin)
# admin.site.register(Location, LocationAdmin)
# admin.site.register(Employee, EmployeeAdmin)
# # admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Supplier, SupplierAdmin)
# admin.site.register(ServiceLookup, ServiceLookupAdmin)
# admin.site.register(ServiceLine, ServiceLineAdmin)
# admin.site.register(Sale, SaleAdmin)
# admin.site.register(SaleLine, SaleLineAdmin)
# admin.site.register(Payroll, PayrollAdmin)
# admin.site.register(PayrollOtherPay, PayrollOtherPayAdmin)
# admin.site.register(Inventory, InventoryAdmin)

# # https://www.youtube.com/watch?v=rxai34qeBcc