from django.conf import settings

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group, Permission
import json
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
#https://stackoverflow.com/questions/48314694/after-login-the-rest-auth-how-to-return-more-information
 

class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = ('__all__')


class CustomerSerializer(serializers.ModelSerializer):
    account_details = AccountDetailsSerializer(many=False, read_only=True)
    class Meta:
        model = Customer
        fields = ('__all__')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # print('instance :>>', instance.objects.values())
        rep["account_details"] = AccountDetailsSerializer(instance.account_details_id, many=False).data
        return rep

class WithdrawalAuthenticationSerializer(serializers.Serializer):
    withdrawal_amount = serializers.IntegerField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    customer = serializers.IntegerField()

    def validate(self, attrs):
        withdrawal_amount = attrs.get('withdrawal_amount', '')
        email = attrs.get('email', False)
        customer = attrs.get('customer', '')
        phone = attrs.get('phone', '')
        
        if not withdrawal_amount:
            raise(serializers.ValidationError('No withdrawal value given'))
        # email = EmailMessage('Test', 'Test', to=['gregory.goufan@gmail.com'])
        # email.send()
        customer_instance = Customer.objects.filter(pk=customer).values()[0]
        send_mail(
            f'Withdrawal Validation: confirmation du retrait de {withdrawal_amount} de votre compte',
            'Here is the message.',
            'gregory.goufan@hotmail.fr', # pay attention here I had a problem because of that
            [email],
            fail_silently=False,
            account_details = AccountDetails.objects.filter(pk=customer_instance['account_details_id_id']).values()[0],
            html_message= render_to_string('withdrawalAuthentication.html', {'account_details': account_details, 'customer':customer_instance,'withdrawal_amount':withdrawal_amount, 'phone': phone})
        )
        return super().validate(attrs) 
    


        
# https://www.django-rest-framework.org/api-guide/relations/
# https://stackoverflow.com/questions/59792488/serializing-nested-objects-in-drfs
# Django Rest Framework API #16 / Many To One Relationship, Nested Data: https://www.youtube.com/watch?v=nB1MczHlweA
# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create