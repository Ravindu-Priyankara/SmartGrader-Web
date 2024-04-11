from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse # use for get json resposes.
from .models import CustomUser #import model
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.forms import AuthenticationForm
import secrets
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import redirect

def generate_session_key(length=32):
    """
    Generate a random session key of specified length.
    """
    return secrets.token_hex(length)

def save_session_key_to_database(session_key, user):
    # Save session key and user details to the database
    session = Session(session_key=session_key)
    session.expire_date = None  # Set the session to never expire

    # Serialize user details
    user_data = {'_auth_user_id': user.id}
    session_data_encoded = Session.encode(user_data)
    session.session_data = session_data_encoded

    session.save()

def get_user_from_session(session_key):
    try:
        # Retrieve session object using session key
        session = Session.objects.get(session_key=session_key)
        
        # Retrieve user ID from session data
        user_id = session.get_decoded().get('_auth_user_id')
        
        # Get User model
        user = CustomUser.objects.get(pk=user_id)
        
        return user
    except (Session.DoesNotExist, KeyError, CustomUser.DoesNotExist):
        return None


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
def login_view(request):
    return render(request, 'login.html')

def login_form_validate(request):
    print(request)
    print(request.user)
    print(request.user.is_authenticated)
    if request.method == 'POST':
        username = request.POST.get('mail')
        password = request.POST.get('password')

        print(username, password)
        
        # Authenticate user against the database
        user = authenticate(request, email=username, password=password)
        
        if user is not None:
            # Credentials are valid
            login(request, user)  # Authenticate the user
            
            # Create a new session or update existing session
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = generate_session_key()

            # Set expiration date for the session
            request.session.set_expiry(timezone.timedelta(days=1))
            #return JsonResponse({'success': True, 'is_authenticated': True, 'session_key': session_key})
            return redirect('/dashboard/?session_key={}'.format(session_key))
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

'''def dashboard(request):
    """if 'user_key' in request.session:
        session_key = request.session['user_key']
        print(session_key)
        return render(request, 'dashboard/index.html')
    else:
        return render(request, 'login.html')"""
    session_key = request.GET.get('session_key')
    if session_key:
        # Session key is available, proceed with the dashboard logic
        # You can also validate the session key here if needed
        print(session_key)
        return render(request, 'dashboard/index.html')
    else:
        # Session key is not provided, handle accordingly
        return render(request, 'login.html')'''

def dashboard(request):
    session_key = request.GET.get('session_key')
    if session_key:
        user = get_user_from_session(session_key)
        if user:
            # Do something with user
            return JsonResponse({'success': True, 'user_details': {'username': user.first_name, 'email': user.email}})
    
    return JsonResponse({'success': False, 'message': 'Failed to retrieve user details'})
    