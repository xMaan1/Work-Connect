from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from .models import User, JobSeekerProfile, CompanyProfile

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
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    location = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'location', 'role', 'password1', 'password2']

class JobSeekerProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    linkedin_url = forms.URLField(required=False)
    website = forms.URLField(required=False)
    resume = forms.FileField(
        required=False,
        widget=forms.FileInput,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    
    class Meta:
        model = JobSeekerProfile
        fields = ['resume', 'skills', 'experience_years', 'education', 'preferred_job_types',
                 'preferred_locations', 'preferred_salary', 'is_available']
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'e.g., Python, JavaScript, React'}),
            'education': forms.Textarea(attrs={'rows': 3}),
            'preferred_job_types': forms.TextInput(attrs={'placeholder': 'e.g., Full-time, Remote'}),
            'preferred_locations': forms.TextInput(attrs={'placeholder': 'e.g., New York, London'}),
            'preferred_salary': forms.TextInput(attrs={'placeholder': 'e.g., $50,000 - $70,000'})
        }

class CompanyProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    linkedin_url = forms.URLField(required=False)
    website = forms.URLField(required=False)
    company_logo = forms.ImageField(required=False, widget=forms.FileInput)
    
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_logo', 'industry', 'company_size', 'founded_year',
                 'company_description', 'company_culture', 'office_locations']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
            'company_culture': forms.Textarea(attrs={'rows': 4}),
            'office_locations': forms.Textarea(attrs={'rows': 2})
        }
