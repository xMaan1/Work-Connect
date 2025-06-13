from django.shortcuts import render

# Create your views here.

def employer_dashboard(request):
    """
    View function for employer dashboard page.
    """
    return render(request, 'employers/dashboard.html', {
        'title': 'Employer Dashboard'
    })
