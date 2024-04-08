from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse # use for get json resposes.
from .models import CustomUser #import model


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

def signup(request): # signup page view
    return render(request, 'signup.html')

def validate_signup(request): #signup validation
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        email = request.POST.get('mail')
        profession = request.POST.get('profession')
        country = request.POST.get('country')
        mobile_number = request.POST.get('number')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Perform validation (Example: Check if passwords match)
        if password != password1:
            return JsonResponse({'success': False, 'message': 'Passwords do not match'}, status=400)
        else:
            # Create new user instance
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                country=country,
                profession=profession,
                number=mobile_number,
                password=password
            )
            
            return JsonResponse({'success': True})
        
def view_users(request):
    # Fetch all registered users from the database
    users = CustomUser.objects.all()

    # Render a template with the list of users
    return render(request, 'users.html', {'users': users})