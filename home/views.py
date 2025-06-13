from django.shortcuts import render
from jobs.models import Job, Category

def home(request):
    recent_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    categories = Category.objects.all()[:6]
    featured_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    return render(request, 'home/index.html', {
        'title': 'Welcome to WorkConnect',
        'recent_jobs': recent_jobs,
        'categories': categories,
        'featured_jobs': featured_jobs
    })
