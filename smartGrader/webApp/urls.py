from django.urls import path
from . import views

#url patterns
urlpatterns = [
    path('',views.index, name='index'), #index page path(landing page)
    path('login/',views.login, name = 'login'), #login page path(landing page)
    path('validate-login/', views.login_form_validate, name = 'validate_login'), # login form validate
    path('signup/',views.signup, name = 'signup'), #login page path(landing page)
    path('validate-signup/', views.validate_signup, name='validate_signup'),
    path('view-users/', views.view_users, name='view_users'),
    path('dashboard/', views.dashboard, name='dashboard'), # dashboard url 
]
