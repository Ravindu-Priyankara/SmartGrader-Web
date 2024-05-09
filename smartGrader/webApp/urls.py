from django.urls import path
from . import views
from .views import dashboard

#url patterns
urlpatterns = [
    path('',views.index, name='index'), #index page path(landing page)
    path('login/', views.login_view, name='login'), #login page path(landing page)
    path('validate-login/', views.login_form_validate, name = 'validate_login'), # login form validate
    path('signup/',views.signup, name = 'signup'), #login page path(landing page)
    path('validate-signup/', views.validate_signup, name='validate_signup'),
    path('view-users/', views.view_users, name='view_users'),
    path('dashboard/', dashboard, name='dashboard'), # dashboard url 
    path('upload/', views.upload_file, name='upload_file'), # upload pdf file
    path('coding/',views.coding_assignment, name = 'coding'),
    path('check/',views.upload_code_file, name = 'check/'),
    path('contact/',views.contact, name = 'contact'),#contact us page url
    path('about/',views.about, name = 'about'),#contact us page url
]
