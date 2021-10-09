from django.urls import path, include
from .views import *
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('department', DepartmentViewSet, 'department')
router.register('salary', SalaryViewSet, 'salary')
router.register('customer', CustomerViewSet, 'customer')
router.register('service', ServiceViewSet, 'service')
router.register('service_lookup', ServiceLookupViewSet, 'service_lookup')
router.register('serviceline', ServiceLineViewSet, 'serviceline')
router.register('city', CityViewSet, 'city')
router.register('location', LocationViewSet, 'location')
router.register('employee', EmployeeViewSet, 'employee')
router.register('category', CategoryViewSet, 'category')
router.register('product', ProductViewSet, 'product')
router.register('supplier', SupplierViewSet, 'supplier')
router.register('sale', SaleViewSet, 'sale')
router.register('saleline', SaleLineViewSet, 'saleline')
router.register('saleslines_by_parent_id', SalesLineByParentIdViewSet, 'saleslines_by_parent_id')
router.register('servicelines_by_parent_id', ServiceLineByParentIdViewSet, 'servicelines_by_parent_id')
router.register('service_by_id', ServiceByIdViewSet, 'service_by_id')

urlpatterns = router.urls

urlpatterns += [
    path('', views.ApiOverview, name="api-overview")
]