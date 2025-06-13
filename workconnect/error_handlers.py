from django.shortcuts import render
from django.core.mail import mail_admins
import traceback

def handler404(request, exception):
    """Custom 404 error handler"""
    context = {
        'error_code': '404',
        'error_title': 'Page Not Found',
        'error_message': "The page you're looking for doesn't exist or has been moved.",
        'error_image': '404.svg',
        'suggestions': [
            'Check that you typed the address correctly',
            'Try searching for what you need using the navigation above',
            'Go back to the previous page and try again'
        ]
    }
    return render(request, 'errors/404.html', context, status=404)

def handler500(request):
    """Custom 500 error handler"""
    # Get the error traceback
    error_traceback = traceback.format_exc()
    
    # Email the error to admins
    subject = 'Server Error on WorkConnect'
    message = f'An error occurred on WorkConnect:\n\n{error_traceback}'
    mail_admins(subject, message, fail_silently=True)
    
    context = {
        'error_code': '500',
        'error_title': 'Server Error',
        'error_message': 'Something went wrong on our end. We have been notified and are working to fix it.',
        'error_image': '500.svg',
        'suggestions': [
            'Try refreshing the page',
            'Come back in a few minutes',
            'Contact support if the problem persists'
        ]
    }
    return render(request, 'errors/500.html', context, status=500)

def handler403(request, exception):
    """Custom 403 error handler"""
    context = {
        'error_code': '403',
        'error_title': 'Access Denied',
        'error_message': "You don't have permission to access this page.",
        'error_image': '403.svg',
        'suggestions': [
            'Make sure youre logged in with the correct account',
            'Contact an administrator if you need access',
            'Return to the homepage'
        ]
    }
    return render(request, 'errors/403.html', context, status=403)
