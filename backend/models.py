from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from descriptive_id.fields import DescriptiveIDField

# Create your models here.

SEXE_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('mixed', 'Mixed'),
)
REGIONS_CHOICES = (
    ('litoral', 'Litoral'),
    ('centre', 'Centre'),
    ('adamawa', 'Adamawa'),
    ('east', 'East'),
    ('north', 'North'),
    ('north_west', 'North West'),
    ('west', 'West'),
    ('south_west', 'South West'),
    ('far_north', 'Far North'),
    ('south', 'South'),
)

class Department(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.name)
class Salary(models.Model):
    percentage = models.PositiveIntegerField(blank=True, null=True,)
    income = models.IntegerField(blank=True, null=True)

    def __str__(self):
        # return str(f'percentage: {self.percentage}, income: {self.income} ')
        # return str(lambda: if self.percentage is None: )
        return str(f'Income: {self.income}') if self.percentage is None  else str(f'percentage: {self.percentage}')


class Customer(models.Model):
    firstname = models.CharField(max_length=100,blank=True, null=True)
    lastname = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(unique=True,blank=True, null=True)
    gender = models.CharField(choices=SEXE_CHOICES, max_length=6, default='male',blank=True,)
    phone_number = models.BigIntegerField(unique=True,blank=True, null=True)

    def __str__(self):
        return str(f'{self.firstname} {self.lastname}')
class City(models.Model):
    name = models.CharField( max_length=12)
    
    # class Meta:
    #     # Add verbose name
    #     verbose_name = 'Citie'
    def __str__(self):
        return str(self.name)
class Street(models.Model):
    name = models.CharField(max_length=24)
    
    def __str__(self):
        return str(self.name)

class Location(models.Model):
    region = models.CharField(choices=REGIONS_CHOICES, max_length=12, default='centre')
    city_id = models.ForeignKey(City, on_delete=models.CASCADE,blank=True,null=True)
    street_id = models.ForeignKey(Street, on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return str(self.region)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, unique=True)
    gender = models.CharField(choices=SEXE_CHOICES, max_length=6, default='male')
    phone_number = models.BigIntegerField(blank=True, null=True)
    department_id = models.ForeignKey(Department, blank=True, null=True,on_delete=models.CASCADE)
    hired_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    location_id = models.ForeignKey(Location, blank=True,null=True, on_delete=models.CASCADE)
    cutomer = models.ManyToManyField(Customer,blank=True,)
    salary_id = models.ForeignKey(Salary, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user.username)

class Category(models.Model):
    name = models.CharField( max_length=150)
    description = models.TextField(blank=True,null=True)
    # class Meta:
    #     # Add verbose name
    #     verbose_name = 'Categorie'
    def __str__(self):
        return str(self.name)

class Supplier(models.Model):
    name = models.CharField( max_length=150)
    company_name = models.CharField( max_length=150,blank=True,null=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE,blank=True,null=True)
    phone_number = models.BigIntegerField(blank=True,null=True)
    email = models.EmailField(max_length = 200,blank=True,null=True)
    
    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True)
    quantity = models.PositiveIntegerField(blank=True,null=True)
    cost_price = models.IntegerField(blank=True,null=True)
    selling_price = models.IntegerField(blank=True,null=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    # https://docs.djangoproject.com/en/2.2/topics/db/examples/many_to_many/
    supplier = models.ManyToManyField(Supplier,blank=True)
    
    def __str__(self):
        return str(self.name)

class Service(models.Model):
    name = DescriptiveIDField(prefix='SERVICE_',
                                         editable=False,
                                         unique=True,
                                         blank=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)
    salary_id = models.ForeignKey(Salary, on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.salary_id  is None:
            self.salary_id = self.employee_id.salary_id
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class ServiceLookup(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class ServiceLine(models.Model):
    parent_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='servicelines', null=True)
    lookup = models.ForeignKey(ServiceLookup, on_delete=models.CASCADE, blank=True, null=True,related_name='lookup')
    # product_id = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_credit = models.BooleanField(help_text='When positive the amount given is paid by the client')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_paid = models.PositiveIntegerField(default=0)
    details = models.TextField(max_length=150, blank=True, null=True)
    payment_method = models.CharField(choices=(('om','Orange Money'),('momo','MTN Money'),),max_length=15)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'N/A' if self.parent_id is None else str(self.parent_id.name)

class Sale(models.Model):
    name = DescriptiveIDField(prefix='SALE_',
                                         editable=False,
                                         unique=True,
                                         blank=False)
    saler_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)   
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)


class SaleLine(models.Model):
    parent_id = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='salelines', null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    product_quantity = models.PositiveIntegerField(blank=True, null=True)
    amount_paid = models.PositiveIntegerField(default=0)
    is_credit = models.BooleanField(help_text='When positive the amount given is paid by the client', default=True)
    details = models.TextField(max_length=150, blank=True, null=True)
    payment_method = models.CharField(choices=(('om','Orange Money'),('momo','MTN Money'),),max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.parent_id.name)