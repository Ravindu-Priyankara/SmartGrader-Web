# forms.py
from django import forms
from django.core.exceptions import ValidationError
import os

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

class FileUploadForm(forms.Form):
    file = forms.FileField()