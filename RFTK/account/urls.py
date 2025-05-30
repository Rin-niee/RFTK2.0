from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register, name='register'),
    path('', login_required(profile), name='profile'),
    path('org/', login_required(org), name='org'),
    path('org/add', login_required(orgadd), name='orgadd'),
    path('org/<int:id>', login_required(orgid), name='orgid'),
    path('clients/', login_required(clients), name='clients'),
    path('clients/add', login_required(clientsadd), name='clientsadd'),
    path('clients/<int:id>', login_required(clientsid), name='clientsid'),
    path('clients/get_counterparties/', get_counterparties, name='get_counterparties'),
    path('clients/get_counterparty_details/', get_counterparty_details, name='get_counterparty_details'),
]
