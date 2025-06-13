from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

# Create your views here.

def user_dashboard(request):
    """
    View function for user dashboard page.
    """
    return render(request, 'users/dashboard.html', {
        'title': 'Dashboard'
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {
        'form': form,
        'title': 'Register for WorkConnect'
    })

@login_required
def dashboard(request):
    if request.user.role == 'employer':
        return redirect('employer_dashboard')
    elif request.user.role == 'seeker':
        return redirect('my_applications')
    else:
        return redirect('admin:index')
