from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse # use for get json resposes.

# Create your views here.

#index page view (landing page)
def index(request):
    return render(request, 'index.html')

# add login page view 
def login(request):
    return render(request, 'login.html')

def login_form_validate(request):
    if request.method == 'POST':
        username = request.POST.get('mail')
        password = request.POST.get('password')
        
        # Perform validation (Example: Check if username and password match)
        if username == 'admin' and password == 'admin':
            # Credentials are valid
            return JsonResponse({'success': True})
        else:
            # Credentials are not valid
            return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)