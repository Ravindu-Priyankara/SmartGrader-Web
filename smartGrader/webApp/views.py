from django.shortcuts import render
from django.template import loader

# Create your views here.

#index page view (landing page)
def index(request):
    return render(request, 'index.html')

# add login page view 
def login(request):
    return render(request, 'login.html')