from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse # use for get json resposes.
from .models import CustomUser #import model
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(forms.Form): #forms validation
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    profession = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    mobile_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Passwords do not match.")


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

        print(username, password)
        
        # Authenticate user against the database
        user = authenticate(request, email=username, password=password)
        
        if user is not None:
            # Credentials are valid
            return JsonResponse({'success': True})
        else:
            # Credentials are not valid
            return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)

def signup(request): # signup page view
    return render(request, 'signup.html')

def validate_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Form is valid, create user
            data = form.cleaned_data
            user = CustomUser.objects.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                country=data['country'],
                profession=data['profession'],
                number=data['mobile_number'],
                password=data['password']
            )
            return JsonResponse({'success': True})
        else:
            # Form is not valid, return errors
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
        
def view_users(request):
    # Fetch all registered users from the database
    users = CustomUser.objects.all()

    # Render a template with the list of users
    return render(request, 'users.html', {'users': users})

# user dashboard
def dashboard(request):
    return render(request, 'dashboard/index.html')