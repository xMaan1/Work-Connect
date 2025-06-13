from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import JobApplication
from jobs.models import Job

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', slug=job.slug)
    
    if request.method == 'POST':
        try:
            application = JobApplication.objects.create(
                job=job,
                applicant=request.user,
                resume=request.FILES['resume'],
                cover_letter=request.POST.get('cover_letter', ''),
                expected_salary=request.POST.get('expected_salary'),
                availability=request.POST.get('availability', '')
            )
            messages.success(request, 'Your application has been submitted successfully!')
            return render(request, 'applications/application_submitted.html', {
                'title': 'Application Submitted',
                'job': job
            })
        except Exception as e:
            messages.error(request, 'There was an error submitting your application. Please try again.')
    
    return render(request, 'applications/apply.html', {
        'title': f'Apply for {job.title}',
        'job': job
    })

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__company')
    
    context = {
        'title': 'My Applications',
        'applications': applications
    }
    return render(request, 'applications/my_applications.html', context)

@login_required
def withdraw_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(
            JobApplication,
            id=application_id,
            applicant=request.user
        )
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Application withdrawn successfully.')
        return redirect('my_applications')
    return redirect('my_applications')
