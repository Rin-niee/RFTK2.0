from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('check/', check, name='check'),
    path('check/add', checkadd, name='checkadd'),
    path('check/<int:id>', checkid, name='checkid'),
    # path('clients/get_counterparties/', get_counterparties, name='get_counterparties'),
    # path('clients/get_counterparty_details/', get_counterparty_details, name='get_counterparty_details'),
]
