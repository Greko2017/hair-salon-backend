from os import name
from django.urls import path, include
from .views import *
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('customer', CustomerViewSet, 'customer')
router.register('account_details', AccountDetailsViewSet, 'account_details')

urlpatterns = router.urls

urlpatterns += [
    path('send_email', WithdrawalAuthenticationView.as_view(), name="send_email"),
    path('', views.ApiOverview, name="api-overview")
]