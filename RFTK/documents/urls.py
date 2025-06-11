from django.urls import path
from .views import *
from account import views as account_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('check/',  login_required(check), name='check'),
    path('check/add',  login_required(checkadd), name='checkadd'),
    path('check/<int:id>',  login_required(checkid), name='checkid'),
    path('check/get_organizations/', get_organizations, name='get_organizations'),
    path('check/get_all_organizations/', get_all_organizations, name='get_all_organizations'),
    path('check/get_organizations_details/', get_organizations_details, name='get_organizations_details'),
    path('check/get_counterparty_details_for_counter/', get_counterparty_details_for_counter, name='get_counterparty_details_for_counter'),
]
