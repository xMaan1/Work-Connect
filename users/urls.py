from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('profile/seeker/edit/', views.update_seeker_profile, name='update_seeker_profile'),
    path('profile/employer/edit/', views.update_employer_profile, name='update_employer_profile'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/users/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
]
