from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

@login_required
def employer_dashboard(request):
    """
    View function for employer dashboard page.
    """
    return render(request, 'employers/dashboard.html', {
        'title': 'Employer Dashboard'
    })

def company_list(request):
    """
    View function for companies list page.
    """
    companies = User.objects.filter(role='employer')
    return render(request, 'employers/company_list.html', {
        'title': 'Companies',
        'companies': companies
    })

@login_required
def post_job(request):
    """
    View function for job posting page.
    """
    if request.method == 'POST':
        # Handle job posting form submission
        pass
    return render(request, 'employers/post_job.html', {
        'title': 'Post a Job'
    })
