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
import io,sys
from .mail import *
from .mailWriter import *

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
        return render(request, 'dashboard/index.html',{'session_key':session_key})
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
    session_key = request.GET.get('session_key')
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

            #print(extracted_text[0])
            name_match = re.search(r'Name\s*=\s*(.*?)\n', extracted_text)
            id_match = re.search(r'Id\s*=\s*(.*?)\n', extracted_text)
            question1_match = re.search(r'1\.(.*?)\n(.*?)\n', extracted_text)
            question2_match = re.search(r'2\.\s*(.*?)\s*?\n\s*(.*?)\n', extracted_text)

            remover('data.log')
            data = get_data(extracted_text)
            plagarism_data = get_plagarism(extracted_text)

            name = name_match.group(1).strip()
            id = id_match.group(1).strip()
            percentage = get_percentage(data)
            plagarism_percentage = get_percentage(plagarism_data)
            decrypted_data = read_encrypted_data()
            radar_values = read_encrypted_data()
            decrypted_data = list(set(decrypted_data))
            count_value = count(radar_values)
            #print(count_value)
            #print(percentage)

            def accuracy_test(marks):
                if marks >= 80:
                    return "excellence"
                elif marks >= 75 and marks < 80:
                    return 'good'
                elif marks >= 60 and marks < 75:
                    return 'accept to pass'
                else:
                    return 'too weak'
            
            accuracy = accuracy_test(percentage)
            

            '''value = check_answer(question1_match.group(0),question1_match.group(1))
            print(value)'''
            mail_address = f"{id}@students.plymouth.ac.uk"
            answers = one_and_zero(data)
            #write html file
            writer("smartGrader/webApp/templates/mail/marks.html",name,id,percentage,data,answers,plagarism_percentage)
            #send mail
            mail(mail_address, "Your Non Coding Assignment Result", "smartGrader/webApp/templates/mail/marks.html")

            return render(request, 'dashboard/student.html',{'percentage_correct': percentage, 'decrypted_data': decrypted_data, 'count':count_value, 'plagarism': plagarism_percentage,
                                                             'name':name, 'id':id, "accuracy":accuracy,'session_key':session_key})

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

def coding_assignment(request):
    session_key = request.GET.get('session_key')
    return render(request, 'dashboard/coding.html',{'session_key':session_key,})

def extract_python_code_from_pdf(pdf_text):
    code_snippets = re.findall(r'def\s+\w+\(.*?\)\s*:\s*.*?(?=def|\Z)', pdf_text, re.DOTALL)
    return code_snippets

def check_code(code_snippets):
    results = []
    for idx, snippet in enumerate(code_snippets, start=1):
        try:
            exec(snippet)
            result = "Passed"  # If execution succeeds, consider it as passed
        except Exception as e:
            result = f"Failed: {e}"  # If execution fails, consider it as failed with the error message
        results.append({"snippet": snippet.strip(), "result": result})
    return results

def check_code_with_expected_output(code_snippets, expected_outputs):
    results = []
    for idx, snippet in enumerate(code_snippets, start=1):
        try:
            # Redirect stdout to capture the output
            sys.stdout = io.StringIO()
            exec(snippet)
            actual_output = sys.stdout.getvalue().strip()  # Get the captured output
            expected_output = expected_outputs[idx - 1].strip()  # Extract the expected output for this snippet
            if actual_output == expected_output:
                result = "Passed"
            else:
                result = f"Failed: Expected output '{expected_output}', but got '{actual_output}'"
        except Exception as e:
            result = f"Failed: {e}"
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__
        results.append(result)
    return results

def upload_code_file(request):
    session_key = request.GET.get('session_key')
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle file upload
            uploaded_file = request.FILES['file']
            uploaded_file2 = request.FILES['file2']
            validate_pdf(uploaded_file)
            validate_pdf(uploaded_file2)
            #convert
            pdf_file1 = uploaded_file
            pdf_file2 = uploaded_file2
            pdf_reader = PdfReader(pdf_file1)
            pdf_reader2 = PdfReader(pdf_file2)
            
            # Extract text from each page
            extracted_text = ''
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

            code_snippets = extract_python_code_from_pdf(extracted_text)
            #print(f"code sinipsets {code_snippets}")
            #results = check_code(code_snippets)
            '''for result in results:
                print(result)'''
            def remove_number_list(text):
                # Define a pattern to match the number list (e.g., "1.", "2.", etc.)
                pattern = r'^\d+\.\s+'
                # Replace the matched pattern with an empty string
                cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
                return cleaned_text
            
            extracted_answers = ''
            for page in pdf_reader2.pages:
                extracted_answers += page.extract_text()
            
            extracted_answers = remove_number_list(extracted_answers)

            expected_outputs = extracted_answers.splitlines()

            # Check code snippets against expected outputs
            results = check_code_with_expected_output(code_snippets, expected_outputs)
            
            # Print or return results as needed
            marks = []
            for result in results:
                if result == "Passed":
                    marks.append('Correct')
                else:
                    marks.append('Incorrect')
            
            
            # Regular expressions to match name, ID, and email
            name_pattern = r'Name\s*:\s*(.*?)\n'
            id_pattern = r'Id\s*:\s*(.*?)\n'
            email_pattern = r'Email\s*:\s*(.*?)\n'

            # Search for matches using regular expressions
            name_match = re.search(name_pattern, extracted_text)
            id_match = re.search(id_pattern, extracted_text)
            email_match = re.search(email_pattern, extracted_text)

            # Extract the matched groups
            name = name_match.group(1).strip() if name_match else None
            id = id_match.group(1).strip() if id_match else None
            email = email_match.group(1).strip() if email_match else None

            percentage = get_percentage(marks)
            #print(count_value)
            #print(percentage)

            def accuracy_test(marks):
                if marks >= 80:
                    return "excellence"
                elif marks >= 75 and marks < 80:
                    return 'good'
                elif marks >= 60 and marks < 75:
                    return 'accept to pass'
                else:
                    return 'too weak'
            
            accuracy = accuracy_test(percentage)

            print(name,id,email,percentage,accuracy)

            decrypted_data = []

            decrypted_data = [i + 1 for i in range(len(marks))]

            count_value = one_and_zero(marks)
            print(count_value)
            print(decrypted_data)
            

            return render(request, 'dashboard/student_code.html',{'session_key':session_key,'percentage_correct': percentage,'name':name, 'id':id,'decrypted_data': decrypted_data
                                                                  , 'decrypted_data': decrypted_data, 'count':count_value})
            #return render(request, 'dashboard/student.html',{'percentage_correct': percentage, 'decrypted_data': decrypted_data, 'count':count_value, 'plagarism': plagarism_percentage,
            #                                                 'name':name, 'id':id, "accuracy":accuracy,'session_key':session_key})

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