from django.urls import path
from . import views

#url patterns
urlpatterns = [
    path('',views.index, name='index'), #index page path(landing page)
    path('login/',views.login, name = 'login'), #login page path(landing page)
    path('validate-login/', views.login_form_validate, name = 'validate_login') # login form validate
]
