from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import UserRegistrationForm, JobSeekerProfileUpdateForm, CompanyProfileUpdateForm
from .models import User, JobSeekerProfile, CompanyProfile, UserAnalytics
from jobs.models import Job
from applications.models import JobApplication

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            welcome_msg = f'Welcome to WorkConnect, {user.first_name}! '
            if user.role == 'seeker':
                welcome_msg += 'Let\'s set up your job seeker profile.'
                redirect_url = 'update_seeker_profile'
            else:
                welcome_msg += 'Let\'s set up your company profile.'
                redirect_url = 'update_employer_profile'
            
            messages.success(request, welcome_msg)
            login(request, user)
            return redirect(redirect_url)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_dashboard(request):
    """
    Route users to their role-specific dashboards
    """
    # Increment analytics
    analytics = request.user.analytics
    analytics.last_login_date = timezone.now()
    analytics.save()
    
    if request.user.role == 'employer':
        return redirect('employer_dashboard')
    elif request.user.role == 'seeker':
        return redirect('seeker_dashboard')
    return redirect('admin:index')

@login_required
def seeker_dashboard(request):
    user = request.user
    if not hasattr(user, 'seeker_profile'):
        JobSeekerProfile.objects.create(user=user)
    
    # Get recent applications
    recent_applications = JobApplication.objects.filter(applicant=user).order_by('-applied_date')[:5]
    
    # Get recommended jobs based on skills
    if user.seeker_profile.skills:
        skills = [s.strip() for s in user.seeker_profile.skills.split(',')]
        recommended_jobs = Job.objects.filter(
            Q(is_active=True) &
            (Q(title__icontains=skills[0]) | Q(description__icontains=skills[0]))
        ).exclude(
            applications__applicant=user
        ).order_by('-created_at')[:5]
    else:
        recommended_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:5]

    # Get analytics
    analytics = user.analytics
    analytics.profile_views += 1
    analytics.save()

    # Add profile completion percentage
    profile = user.seeker_profile
    total_fields = 10  # Adjust based on your profile model
    filled_fields = sum(bool(getattr(profile, field.name)) for field in profile._meta.fields if field.name != 'id' and field.name != 'user')
    completion = (filled_fields / total_fields) * 100

    context = {
        'user': user,
        'profile_completion': int(completion),
        'recent_applications': recent_applications,
        'recommended_jobs': recommended_jobs,
        'analytics': analytics,
        'title': 'Dashboard'
    }
    
    return render(request, 'users/seeker_dashboard.html', context)

@login_required
def employer_dashboard(request):
    user = request.user
    if not hasattr(user, 'company_profile'):
        CompanyProfile.objects.create(user=user)
    
    # Get recent job postings
    recent_jobs = Job.objects.filter(company=user).order_by('-created_at')[:5]
    
    # Get recent applications to your jobs
    recent_applications = JobApplication.objects.filter(
        job__company=user
    ).order_by('-applied_date')[:5]

    # Get analytics
    analytics = user.analytics
    analytics.profile_views += 1
    analytics.save()

    # Add profile completion percentage
    profile = user.company_profile
    total_fields = 8  # Adjust based on your profile model
    filled_fields = sum(bool(getattr(profile, field.name)) for field in profile._meta.fields if field.name != 'id' and field.name != 'user')
    completion = (filled_fields / total_fields) * 100

    context = {
        'user': user,
        'profile_completion': int(completion),
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
        'analytics': analytics,
        'title': 'Employer Dashboard'
    }
    
    return render(request, 'users/employer_dashboard.html', context)

@login_required
def update_seeker_profile(request):
    user = request.user
    if request.method == 'POST':
        form = JobSeekerProfileUpdateForm(request.POST, request.FILES, instance=user.seeker_profile)
        if form.is_valid():
            # Update user fields
            for field in ['avatar', 'bio', 'linkedin_url', 'website']:
                if field in request.POST:
                    setattr(user, field, request.POST.get(field))
                if field in request.FILES:
                    setattr(user, field, request.FILES[field])
            user.save()
            
            # Save profile
            profile = form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('seeker_dashboard')
    else:
        form = JobSeekerProfileUpdateForm(instance=user.seeker_profile)
    
    context = {
        'form': form,
        'user': user,
        'title': 'Edit Profile'
    }
    return render(request, 'users/edit_seeker_profile.html', context)

@login_required
def update_employer_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CompanyProfileUpdateForm(request.POST, request.FILES, instance=user.company_profile)
        if form.is_valid():
            # Update user fields
            for field in ['avatar', 'bio', 'linkedin_url', 'website']:
                if field in request.POST:
                    setattr(user, field, request.POST.get(field))
                if field in request.FILES:
                    setattr(user, field, request.FILES[field])
            user.save()
            
            # Save profile
            profile = form.save()
            messages.success(request, 'Your company profile has been updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = CompanyProfileUpdateForm(instance=user.company_profile)
    
    context = {
        'form': form,
        'user': user,
        'title': 'Edit Company Profile'
    }
    return render(request, 'users/edit_employer_profile.html', context)
