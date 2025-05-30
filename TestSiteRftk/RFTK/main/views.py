from django.shortcuts import render
from django.urls import path
from .views import *


# Create your views here.
def index(request):
    return render(request, 'main/index.html')