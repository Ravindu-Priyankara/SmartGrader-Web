from django.contrib.auth.decorators import login_required as auth_login_required
from django.shortcuts import redirect

def login_required_decorator(view_func):
    def wrapped_view(request, *args, **kwargs):
        print(request)
        is_authenticated = kwargs.pop('is_authenticated', False)  # Get the value of is_authenticated from kwargs
        print(is_authenticated)
        if not is_authenticated:
            print(is_authenticated)
            return redirect('login')  # Redirect to your login page
        return view_func(request, *args, **kwargs)
    return wrapped_view


