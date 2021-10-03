# Create your views here.
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import viewsets, permissions, generics, status
from django.contrib.auth.models import User, Group, Permission

from .models import *
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Customer List': '/customer/',
        'Customer Detail': '/customer/<str:pk>/',
    }
    return Response(api_urls)
    
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')

    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.all().order_by('-id')
        
class AccountDetailsViewSet(viewsets.ModelViewSet):
    queryset = AccountDetails.objects.all().order_by('-id')

    serializer_class = AccountDetailsSerializer

    def get_queryset(self):
        return AccountDetails.objects.all().order_by('-id')

class WithdrawalAuthenticationView(generics.GenericAPIView):
    serializer_class = WithdrawalAuthenticationSerializer
    def post(self, request):
        email_data_temp = request.data
        serializer = self.serializer_class(data=email_data_temp)
        serializer.is_valid(raise_exception=True)

        email_data = serializer.data
        return Response(email_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        return render(request=request, template_name='withdrawalAuthentication.html',)

        