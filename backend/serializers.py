from django.conf import settings

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group, Permission
import json
from django.contrib.contenttypes.models import ContentType
#https://stackoverflow.com/questions/48314694/after-login-the-rest-auth-how-to-return-more-information


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'username',
            'last_name',
            'groups',
            'user_permissions',
        )  #'username'
        depth = 1

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('__all__')

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ('__all__')
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')

class ServiceLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLookup
        fields = ('__all__')

class ServiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLine
        fields = ('__all__')
        depth = 2
        
        def create(self, validated_data):
            # print('-- In ServiceLineSerializer create', validated_data)
            customer_id = validated_data.get("customer_id", None)
            lookup = validated_data.get("lookup", None)
            # Once you are done, create the instance with the validated data
            return ServiceLine.objects.create(customer_id=customer_id, lookup=lookup, **validated_data)

        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('__all__')
        depth = 2

class ServiceSerializer(serializers.ModelSerializer):
    servicelines = ServiceLineSerializer(many=True, read_only=True)
    # employee_id = EmployeeSerializer(many=False, read_only=True)
    class Meta:
        model = Service
        fields = ('__all__')
        # exclude = ('permissions', )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["employee"] = EmployeeSerializer(instance.employee_id, many=False).data
        try:
          employee_id = Employee.objects.get(user=instance.created_by.id)
          rep["owner"] = EmployeeSerializer(employee_id, many=False).data
        except Exception as e:
          print("An exception occurred: ", e) 
        return rep

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('__all__')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('__all__')
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["category"] = CategorySerializer(instance.category_id, many=False).data
        return rep
        
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('__all__')
        
class SaleLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleLine
        fields = ('__all__')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["parent"] = SaleSerializer(instance.parent_id, many=False).data
        rep["product"] = ProductSerializer(instance.product_id, many=False).data
        return rep
        

class SaleSerializer(serializers.ModelSerializer):
    # salelines = SaleLineSerializer(many=True, read_only=True)
    class Meta:
        model = Sale
        fields = ('__all__')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["saler"] = EmployeeSerializer(instance.saler_id, many=False).data
        rep["customer"] = CustomerSerializer(instance.customer_id, many=False).data
                        
        saleline_queryset = list(SaleLine.objects.filter(parent_id=instance.id).values())
        # print('In SaleSerializer', saleline_queryset)
        for item in saleline_queryset:
            item['parent'] = Sale.objects.filter(id=item['parent_id_id']).values().first()
            item['product'] = Product.objects.filter(id=item['product_id_id']).values().first()
            
        rep['salelines'] = saleline_queryset

        return rep
        
class PayrollOtherPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollOtherPay
        fields = ('__all__')
        depth = 2
        
    def validate(self, data):
        """
        Take parent parameter and pass it to validated data
        """
        # print('--- PayrollOtherPay validate', self.initial_data)
        parent_id = self.initial_data.get('parent', None)
        if parent_id is not None:
            parent = Payroll.objects.get(id=parent_id)
            data['parent'] = parent
        # print('--- PayrollOtherPay data', data)
        return data

    def create(self, validated_data):
        return PayrollOtherPay.objects.create(**validated_data)

        
class PayrollDeductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayrollDeduction
        fields = ('__all__')
        depth = 2

    def validate(self, data):
        """
        Take parent parameter and pass it to validated data
        """
        parent_id = self.initial_data.get('parent', None)
        if parent_id is not None:
            parent = Payroll.objects.get(id=parent_id)
            data['parent'] = parent
        return data

    # def create(self, validated_data):
    #     parent = validated_data.get("parent", None)
    #     return PayrollDeduction.objects.create(parent=parent, **validated_data)

        
class PayrollSerializer(serializers.ModelSerializer):
    other_pays = PayrollOtherPaySerializer(many=True, read_only=True)
    deductions = PayrollDeductionSerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["employee"] = EmployeeSerializer(instance.employee, many=False).data
        rep['owner'] = User.objects.filter(id=instance.created_by.id).values().first()
        return rep
    class Meta:
        model = Payroll
        fields = ('id', 'created_at','name','status','date_from', 'date_to', 'worked_value', 'computed_salary', 'employee', 'net_salary','other_pays','deductions',)


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('__all__')
        depth = 2

    def validate(self, data):
        """
        Take parent parameter and pass it to validated data
        """
        product = self.initial_data.get('product', None)
        if product is not None:
            product = Product.objects.get(id=product)
            data['product'] = product
        return data
# https://www.django-rest-framework.org/api-guide/relations/
# https://stackoverflow.com/questions/59792488/serializing-nested-objects-in-drfs
# Django Rest Framework API #16 / Many To One Relationship, Nested Data: https://www.youtube.com/watch?v=nB1MczHlweA
# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create