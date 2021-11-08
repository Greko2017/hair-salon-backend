# Create your views here.
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User, Group, Permission

from .models import *
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from django.core import serializers
# https://stackoverflow.com/questions/54544978/customizing-jwt-response-from-django-rest-framework-simplejwt
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        data['user'] = UserSerializer(self.user).data

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
# https://pypi.org/project/djangorestframework-simplejwt/3.2.2/
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'List': '/station-list/',
        'Detail View': '/station-detail/<str:pk>/',
        'Create': '/station-create/',
        'Update': '/station-update/<str:pk>/',
        'Delete': '/station-delete/<str:pk>/',
    }

#     return Response(api_urls)

# class DepartmentViewSet(viewsets.ModelViewSet):
#     queryset = Department.objects.all().order_by('-id')

#     serializer_class = DepartmentSerializer

#     def get_queryset(self):
#         return Department.objects.all().order_by('-id')

# class SalaryViewSet(viewsets.ModelViewSet):
#     queryset = Salary.objects.all().order_by('-id')

#     serializer_class = SalarySerializer

#     def get_queryset(self):
#         return Salary.objects.all().order_by('-id')
        
# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all().order_by('-id')

#     serializer_class = CustomerSerializer

#     def get_queryset(self):
#         return Customer.objects.all().order_by('-id')
        
# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all().order_by('-id')

#     serializer_class = ServiceSerializer

#     def get_queryset(self):
#         return Service.objects.all().order_by('-id')
    
#     def perform_create(self, serializer):
#         user = None
#         if self.request and hasattr(self.request, "user"):
#             user = self.request.user
#         serializer.save(created_by=user)
        
# class ServiceLineViewSet(viewsets.ModelViewSet):
#     queryset = ServiceLine.objects.all().order_by('-id')

#     serializer_class = ServiceLineSerializer

#     def get_queryset(self):
#         return ServiceLine.objects.all().order_by('-id')
    
#     def create(self, request, *args, **kwargs):
#         service_data = request.data
#         lookup = ServiceLookup.objects.get(id=service_data["lookup"])
#         customer_id = Customer.objects.get(id=service_data["customer_id"])
#         parent_id = Service.objects.get(id=service_data["parent_id"])

#         new_car = ServiceLine.objects.create(parent_id=parent_id,lookup=lookup, customer_id=customer_id, amount_paid=service_data[
#             "amount_paid"], is_credit=service_data["is_credit"], payment_method=service_data["payment_method"], quantity=service_data["quantity"])

#         new_car.save()

#         serializer = ServiceLineSerializer(new_car)

#         return Response(serializer.data)

        
#     def update(self, request, *args, **kwargs):
#         serviceline_object = self.get_object()
#         data = request.data
#         # print('-- in  ServiceLineViewSet',data)

#         lookup = ServiceLookup.objects.get(id=data["lookup"])
#         customer_id = Customer.objects.get(id=data["customer_id"])

#         serviceline_object.lookup = lookup
#         serviceline_object.customer_id = customer_id
#         serviceline_object.amount_paid = data["amount_paid"]
#         serviceline_object.id = data["id"]
#         serviceline_object.is_credit = data["is_credit"]
#         serviceline_object.payment_method = data["payment_method"]
#         serviceline_object.quantity = data["quantity"] 

#         serviceline_object.save()

#         serializer = ServiceLineSerializer(serviceline_object)

#         return Response(serializer.data)
        
# class ServiceLookupViewSet(viewsets.ModelViewSet):
#     queryset = ServiceLookup.objects.all().order_by('-id')

#     serializer_class = ServiceLookupSerializer

#     def get_queryset(self):
#         return ServiceLookup.objects.all().order_by('-id')

# class CityViewSet(viewsets.ModelViewSet):
#     queryset = City.objects.all().order_by('-id')

#     serializer_class = CitySerializer

#     def get_queryset(self):
#         return City.objects.all().order_by('-id')
        
# class LocationViewSet(viewsets.ModelViewSet):
#     queryset = Location.objects.all().order_by('-id')

#     serializer_class = LocationSerializer

#     def get_queryset(self):
#         return Location.objects.all().order_by('-id')
        
# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all().order_by('-id')

#     serializer_class = EmployeeSerializer

#     def get_queryset(self):
#         return Employee.objects.all().order_by('-id')
        
# # class CategoryViewSet(viewsets.ModelViewSet):
# #     queryset = Category.objects.all().order_by('-id')

# #     serializer_class = CategorySerializer

# #     def get_queryset(self):
# #         return Category.objects.all().order_by('-id')
        
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all().order_by('-id')

#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         return Product.objects.all().order_by('-id')
        
# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all().order_by('-id')

#     serializer_class = SupplierSerializer

#     def get_queryset(self):
#         return Supplier.objects.all().order_by('-id')
        
# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all().order_by('-id')

#     serializer_class = SupplierSerializer

#     def get_queryset(self):
#         return Supplier.objects.all().order_by('-id')
        
# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all().order_by('-id')

#     serializer_class = SupplierSerializer

#     def get_queryset(self):
#         return Supplier.objects.all().order_by('-id')
        
# class SaleViewSet(viewsets.ModelViewSet):
#     queryset = Sale.objects.all().order_by('-id')

#     serializer_class = SaleSerializer

#     def get_queryset(self):
#         return Sale.objects.all().order_by('-id')
        
# class SaleLineViewSet(viewsets.ModelViewSet):
#     queryset = SaleLine.objects.all().order_by('-id')

#     serializer_class = SaleLineSerializer

#     def get_queryset(self):
#         return SaleLine.objects.all().order_by('-id')

# class ServiceLineByParentIdViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         request = self.request
#         queryset = ServiceLine.objects.all()
#         print('In ServiceLineByParentIdViewSet get_queryset',
#               request.GET.get('parent_id', None))
#         parent_id = request.GET.get('parent_id', None)
#         income_lines = get_list_or_404(queryset, parent_id=parent_id)
#         print('In ServiceLineByParentIdViewSet get_queryset', income_lines)
#         return income_lines

#     serializer_class = ServiceLineSerializer


# class ServiceByIdViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         request = self.request
#         queryset = Service.objects.all()
#         print('In ServiceByIdViewSet get_queryset',
#               request.GET.get('parent_id', None))
#         parent_id = request.GET.get('parent_id', None)
#         income_lines = get_list_or_404(queryset, parent_id=parent_id)
#         print('In ServiceByIdViewSet get_queryset', income_lines)
#         return income_lines

#     serializer_class = ServiceSerializer


# class SalesLineByParentIdViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         request = self.request
#         queryset = SaleLine.objects.all()
#         parent_id = request.GET.get('parent_id', None)
#         income_lines = get_list_or_404(queryset, parent_id=parent_id)
#         return income_lines

#     serializer_class = SaleLineSerializer
    
# class PayrollViewSet(viewsets.ModelViewSet):
#     queryset = Payroll.objects.all().order_by('-id')

#     serializer_class = PayrollSerializer

#     def get_queryset(self):
#         return Payroll.objects.all().order_by('-id')
    
#     def perform_create(self, serializer):
#         user = None
#         if self.request and hasattr(self.request, "user"):
#             user = self.request.user
#         serializer.save(created_by=user)
        
# class PayrollOtherPayViewSet(viewsets.ModelViewSet):
#     queryset = PayrollOtherPay.objects.all().order_by('-id')

#     serializer_class = PayrollOtherPaySerializer

#     def get_queryset(self):
#         return PayrollOtherPay.objects.all().order_by('-id')
        
# class PayrollDeductionViewSet(viewsets.ModelViewSet):
#     queryset = PayrollDeduction.objects.all().order_by('-id')

#     serializer_class = PayrollDeductionSerializer

#     def get_queryset(self):
#         return PayrollDeduction.objects.all().order_by('-id')


# class PayrollOtherPayByParentIdViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         request = self.request
#         queryset = PayrollOtherPay.objects.all()
#         parent_id = request.GET.get('parent_id', None)
#         income_lines = get_list_or_404(queryset, parent_id=parent_id)
#         return income_lines

#     serializer_class = PayrollOtherPaySerializer
    
# class PayrollDeductionByParentIdViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         request = self.request
#         queryset = PayrollDeduction.objects.all()
#         parent_id = request.GET.get('parent_id', None)
#         income_lines = get_list_or_404(queryset, parent_id=parent_id)
#         return income_lines

#     serializer_class = PayrollDeductionSerializer
    
# class PayrollToApproveViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         request = self.request
#         queryset = Payroll.objects.all()
#         payroll_to_approve = get_list_or_404(queryset, employee__user=request.user, status='to_approve')
#         return payroll_to_approve

#     serializer_class = PayrollSerializer

# class InventoryViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     serializer_class = InventorySerializer

#     def get_queryset(self):
#         return Inventory.objects.all().order_by('-id')