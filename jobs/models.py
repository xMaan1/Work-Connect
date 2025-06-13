from django.db import models
from django.utils import timezone
from users.models import CompanyProfile

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Job(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead'),
        ('manager', 'Manager'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs')
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    benefits = models.TextField(blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    skills_required = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

    @property
    def is_expired(self):
        return timezone.now() > self.deadline

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'deadline', 'is_active']),
            models.Index(fields=['location']),
            models.Index(fields=['employment_type']),
        ]
