from django.conf import settings

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group, Permission
import json
from django.contrib.contenttypes.models import ContentType
#https://stackoverflow.com/questions/48314694/after-login-the-rest-auth-how-to-return-more-information


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
        
# https://www.django-rest-framework.org/api-guide/relations/
# https://stackoverflow.com/questions/59792488/serializing-nested-objects-in-drfs
# Django Rest Framework API #16 / Many To One Relationship, Nested Data: https://www.youtube.com/watch?v=nB1MczHlweA
# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create