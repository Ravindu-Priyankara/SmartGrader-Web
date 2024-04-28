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
from .forms import FileUploadForm
from .forms import validate_pdf
from PyPDF2 import PdfReader

import re
from .aiModel import *



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
            request.session.set_expiry(timezone.timedelta(hours=1))
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

def dashboard(request):
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
        return render(request, 'login.html')

'''def dashboard(request):
    session_key = request.GET.get('session_key')
    if session_key:
        user = get_user_from_session(session_key)
        if user:
            # Do something with user
            return JsonResponse({'success': True, 'user_details': {'username': user.first_name, 'email': user.email}})
    
    return JsonResponse({'success': False, 'message': 'Failed to retrieve user details'})
    
    
    def dashboard(request):
    if 'user_key' in request.session:
        session_key = request.session['user_key']
        user = CustomUser.objects.get(session_key=session_key)
        return render(request, 'dashboard/index.html', {'user': user})
    else:
        return render(request, 'login.html')'''



def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle file upload
            uploaded_file = request.FILES['file']
            validate_pdf(uploaded_file)
            #convert
            pdf_file = uploaded_file
            # Read the PDF file
            pdf_reader = PdfReader(pdf_file)
            # Extract text from each page
            extracted_text = ''
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

            print(extracted_text[0])
            name_match = re.search(r'Name\s*=\s*(.*?)\n', extracted_text)
            id_match = re.search(r'Id\s*=\s*(.*?)\n', extracted_text)
            question1_match = re.search(r'1\.(.*?)\n(.*?)\n', extracted_text)
            question2_match = re.search(r'2\.\s*(.*?)\s*?\n\s*(.*?)\n', extracted_text)

            
            data = get_data(extracted_text)

            name = name_match.group(1).strip()
            id = id_match.group(1).strip()
            percentage = get_percentage(data)
            

            '''value = check_answer(question1_match.group(0),question1_match.group(1))
            print(value)'''

            return render(request, 'dashboard/student.html',{'percentage_correct': percentage})

             # Use regular expressions to find specific data
            '''
            name_match = re.search(r'Name\s*=\s*(.*?)\n', extracted_text)
            id_match = re.search(r'Id\s*=\s*(.*?)\n', extracted_text)
            question1_match = re.search(r'1\.(.*?)\n(.*?)\n', extracted_text)
            question2_match = re.search(r'2\.(.*?)\n(.*?)\n', extracted_text)
            if name_match and id_match and question1_match and question2_match:
                name = name_match.group(1)
                id = id_match.group(1)
                question1 = question1_match.group(1)
                answer1 = question1_match.group(2)
                question2 = question2_match.group(1)
                #answer2 = question2_match.group(2)
                return render(request, 'success.html', {'name': name, 'id': id, 'question1': question1, 'answer1': answer1, 'question2': question2})
            else:
                error_message = "Failed to extract data from the PDF. Make sure the format matches the expected pattern."
                return render(request, 'index.html', {'error_message': error_message})'''
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
    