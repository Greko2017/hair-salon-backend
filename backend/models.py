from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey
from django.db.models.query_utils import select_related_descend
from descriptive_id.fields import DescriptiveIDField
from datetime import datetime
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

STATUS = (('draft', 'Draft'), ('to_approve', 'To Approve'),
                 ('approve', 'Approve'), ('un_approve', 'Un Approve'))

class Department(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.name)
class Salary(models.Model):
    percentage = models.PositiveIntegerField(blank=True, null=True,)
    income = models.IntegerField(blank=True, null=True)
    is_percentage = models.BooleanField(default=False)

    def __str__(self):
        # return str(f'percentage: {self.percentage}, income: {self.income} ')
        # return str(lambda: if self.percentage is None: )
        return str(f'Income: {self.income}') if not self.is_percentage   else str(f'percentage: {self.percentage}')


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
    
    class Meta:
        # Add verbose name
        verbose_name = 'Citie'
        verbose_name_plural = 'Cities'

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

# class Category(models.Model):
#     name = models.CharField( max_length=150)
#     description = models.TextField(blank=True,null=True)
#     # class Meta:
#     #     # Add verbose name
#     #     verbose_name = 'Categorie'
#     def __str__(self):
#         return str(self.name)

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
    # category_id = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
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

    def get_total_amount_paid(self):
        tmp_total_amount_paid = 0
        for serviceline in self.servicelines.all():
            # print('-- In get_total_amount_paid',tmp_total_amount_paid)
            tmp_total_amount_paid = tmp_total_amount_paid + serviceline.amount_paid
        return tmp_total_amount_paid

    total_amount_paid = property(get_total_amount_paid)

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

class Payroll(models.Model):
    def _get_payroll_name(self):
        return f"SlIP_{self.date_to}"

    name = DescriptiveIDField(prefix='SLIP_',
                                         editable=False,
                                         null=True,
                                         unique=True,
                                         blank=False)

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='payrolls', null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=12, default='draft')

    class Meta:
        permissions = (
            ("payslip_can_approve", "Can approve payslip"),
            ("payslip_can_un_approve", "Can un approve payslip"),
            ("can_send_for_approval", "Can Send For Approval"),
        )

    def save(self, *args, **kwargs):
        if self.name  is None:
            self.name = f"SLIP_{datetime.now().strftime('%Y%m%d%H%M%S')}" #%f
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.employee.user.username, self.net_salary)
    
    def _get_net_salary(self):
        "Returns the employee's net salary."
        extras = 0
        # print('--- _get_net_salary other_pays', self.other_pays.all())
        for extra in self.other_pays.all():
            # print('--- _get_net_salary extra', extra)
            if extra.amount >= 0:
                extras = extras + extra.amount
        deductions = 0
        for deduction in self.deductions.all():
            if deduction.amount >= 0:
                deductions = deductions + deduction.amount
        # print(f'--- extra : {extras} deduction : {deductions}')

        net_salary = self.computed_salary + extras - deductions
        return net_salary

    def _get_computed_salary(self):
        computed_salary = 0
        income = self.employee.salary_id.income
        percentage = self.employee.salary_id.percentage
        is_percentage = self.employee.salary_id.is_percentage
        if is_percentage == True:
            services = Service.objects.filter(created__range=(self.date_from, self.date_to), employee_id=self.employee.id)
            # print('--- _get_computed_salary services',self.employee, services)
            for service in services:
                tmp_total_amount_paid = 0
                for serviceline in service.servicelines.all():
                    # print('-- In serviceline',serviceline.id, serviceline.amount_paid)
                    tmp_total_amount_paid = tmp_total_amount_paid + serviceline.amount_paid
                computed_salary = computed_salary + tmp_total_amount_paid
            return (computed_salary*percentage) / 100
        else:
            computed_salary = income

        return computed_salary

    def _get_worked_value_in_period(self):
        worked_value = 0
        income = self.employee.salary_id.income
        if income is None:
            services = Service.objects.filter(created__range=(self.date_from, self.date_to), employee_id=self.employee.id)
            # print('--- _get_worked_value services',self.employee, services)
            for service in services:
                tmp_total_amount_paid = 0
                for serviceline in service.servicelines.all():
                    # print('-- In serviceline',serviceline.id, serviceline.amount_paid)
                    tmp_total_amount_paid = tmp_total_amount_paid + serviceline.amount_paid
                worked_value = worked_value + tmp_total_amount_paid
        return worked_value

    net_salary = property(_get_net_salary)
    computed_salary = property(_get_computed_salary)
    worked_value = property(_get_worked_value_in_period)
    
class PayrollOtherPay(models.Model):
    parent = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='other_pays', null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class PayrollDeduction(models.Model):
    parent = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deductions', null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# https://stackoverflow.com/questions/17682567/how-to-add-a-calculated-field-to-a-django-model
    
class Inventory(models.Model):
    name = models.CharField(blank=True,null=True,max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.PositiveIntegerField(blank=True,null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=12, default='draft')

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        if self.name  is None:
            self.name = f"INV_{datetime.now().strftime('%Y%m%d%H%M%S')}" #%f
        super().save(*args, **kwargs)
        
    class Meta:
        permissions = (
            ("user_inventory", "User Inventory"),
            ("management_inventory", "Manager inventory"),
        )