from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Job, Category
from applications.models import JobApplication

def job_list(request):
    """
    View function for listing all jobs.
    """
    jobs = Job.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Search and filtering
    query = request.GET.get('q')
    category = request.GET.get('category')
    location = request.GET.get('location')
    employment_type = request.GET.get('type')
    experience_level = request.GET.get('experience')
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__company_name__icontains=query)
        )
    
    if category:
        jobs = jobs.filter(category__slug=category)
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    
    if experience_level:
        jobs = jobs.filter(experience_level=experience_level)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    context = {
        'title': 'Browse Jobs',
        'jobs': jobs,
        'categories': categories,
        'employment_types': Job.EMPLOYMENT_TYPE_CHOICES,
        'experience_levels': Job.EXPERIENCE_LEVEL_CHOICES,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, slug):
    """
    View function for showing job details.
    """
    job = get_object_or_404(Job, slug=slug, is_active=True)
    
    # Increment view count
    job.views_count += 1
    job.save()
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(
            job=job,
            applicant=request.user
        ).exists()
    
    similar_jobs = Job.objects.filter(
        Q(category=job.category) |
        Q(company=job.company)
    ).exclude(id=job.id)[:3]
    
    context = {
        'title': job.title,
        'job': job,
        'has_applied': has_applied,
        'similar_jobs': similar_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)
