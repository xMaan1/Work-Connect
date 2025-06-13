from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils import timezone

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
    headline = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def get_absolute_url(self):
        return reverse('profile_view', kwargs={'username': self.username})

    def get_dashboard_url(self):
        if self.role == 'employer':
            return reverse('employer_dashboard')
        elif self.role == 'seeker':
            return reverse('seeker_dashboard')
        return reverse('admin:index')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    skills = models.TextField(blank=True, help_text="Comma separated list of skills")
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    preferred_job_types = models.CharField(max_length=100, blank=True)
    preferred_locations = models.CharField(max_length=200, blank=True)
    preferred_salary = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    industry = models.CharField(max_length=100)
    company_size = models.CharField(max_length=50)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    company_description = models.TextField(blank=True)
    company_culture = models.TextField(blank=True)
    office_locations = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class UserAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    profile_views = models.PositiveIntegerField(default=0)
    last_login_date = models.DateTimeField(default=timezone.now)
    total_applications = models.PositiveIntegerField(default=0)
    total_job_posts = models.PositiveIntegerField(default=0)
    application_success_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Analytics"

def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        UserAnalytics.objects.create(user=instance)
        if instance.role == 'seeker':
            JobSeekerProfile.objects.create(user=instance)
        elif instance.role == 'employer':
            CompanyProfile.objects.create(user=instance)

# Connect the signal
from django.db.models.signals import post_save
post_save.connect(create_user_profiles, sender=User)
