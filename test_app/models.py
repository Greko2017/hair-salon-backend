from django.db import models

# Create your models here.

SEXE_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('mixed', 'Mixed'),
)
STATUS = (
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)


class AccountDetails(models.Model):
    account_number = models.CharField(max_length=24)
    amount = models.IntegerField( null=True)
    status = models.CharField(choices=STATUS, max_length=12, default='draft',blank=True,)
    def __str__(self):
        return str(f'{self.account_number}: {self.amount}')


class Customer(models.Model):
    firstname = models.CharField(max_length=100,blank=True, null=True)
    lastname = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(unique=True,blank=True, null=True)
    gender = models.CharField(choices=SEXE_CHOICES, max_length=6, default='male',blank=True,)
    phone_number = models.BigIntegerField(unique=True,blank=True, null=True)
    account_details_id = models.ForeignKey(AccountDetails, related_name="account_details", on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(f'{self.firstname} {self.lastname}')