from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('seeker', 'Job Seeker'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True
    )
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100)
    company_size = models.CharField(max_length=50, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'
