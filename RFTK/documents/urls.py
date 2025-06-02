from django.urls import path
from .views import *
from account import views as account_views

urlpatterns = [
    path('check/', check, name='check'),
    path('check/add', checkadd, name='checkadd'),
    path('check/<int:id>', checkid, name='checkid'),
    path('check/get_organizations/', get_organizations, name='get_organizations'),
    path('check/get_all_organizations/', get_all_organizations, name='get_all_organizations'),
    path('check/get_organizations_details/', get_organizations_details, name='get_organizations_details'),
    path('check/get_counterparty_details_for_counter/', get_counterparty_details_for_counter, name='get_counterparty_details_for_counter'),
]
