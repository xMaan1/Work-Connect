from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.urls import reverse
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
    applied_date = models.DateTimeField(default=timezone.now)
    resume = models.FileField(
        upload_to='applications/resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True
    )
    cover_letter = models.TextField(blank=True)
    general_notes = models.TextField(blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date']
        unique_together = ['job', 'applicant']

    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.job.title}"

    def get_absolute_url(self):
        return reverse('application_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.status != 'pending' and not self.review_date:
            self.review_date = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.status in ['pending', 'reviewing', 'shortlisted', 'interviewing', 'offered']

    @property
    def status_color(self):
        return {
            'pending': 'secondary',
            'reviewing': 'info',
            'shortlisted': 'primary',
            'interviewing': 'warning',
            'offered': 'success',
            'accepted': 'success',
            'rejected': 'danger',
            'withdrawn': 'dark'
        }.get(self.status, 'secondary')

class ApplicationNote(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.author.get_full_name()} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
