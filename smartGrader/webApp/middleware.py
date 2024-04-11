# middleware.py
from django.contrib.auth import authenticate, login

class UpdateAuthStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before it reaches the view
        response = self.process_request(request)

        # If the response is None, continue processing the request
        if response is None:
            response = self.get_response(request)

        # Return the response
        return response

    def process_request(self, request):
        # Update request.user.is_authenticated if the user is logged in
        username = request.POST.get('mail')
        password = request.POST.get('password')

        print(username, password)
        
        # Authenticate user against the database
        user = authenticate(request, email=username, password=password)
        login(request, user)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            request.user.is_authenticated = True

        # Return None to continue processing the request
        return None
