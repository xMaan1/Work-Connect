from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from jobs.models import Job

User = get_user_model()

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewing', 'Interviewing'),
        ('offered', 'Offer Extended'),
        ('accepted', 'Offer Accepted'),
        ('rejected', 'Not Selected'),
        ('withdrawn', 'Application Withdrawn')
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    resume = models.FileField(
        upload_to='applications/resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='PDF files only'
    )
    cover_letter = models.TextField(blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    employer_notes = models.TextField(blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
