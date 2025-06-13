from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('companies/', views.company_list, name='companies'),
    path('post-job/', views.post_job, name='post_job'),
]
