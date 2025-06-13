from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('employer', 'I want to post jobs (Employer)'),
        ('seeker', 'I want to find jobs (Job Seeker)'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Account Type'
    )
    
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
