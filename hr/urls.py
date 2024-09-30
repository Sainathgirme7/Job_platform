from django.urls import path
from hr import views
from main.views import contact

urlpatterns = [
    path('hrdash/', views.hrHome, name='hrdash'),  # HR Dashboard view
    path('candidatedetails/<int:id>/', views.hrCandidateDetails, name='candidatedetails'),  # View for candidate details
    path('postjob/', views.postJobs, name='postjob'),  # View for posting a job
    path('acceptapplication/', views.acceptApplication, name='acceptapplication'),  # View for accepting a job application
    path('rejectapplication/', views.rejectApplication, name='rejectapplication'),  # View for rejecting a job application
    path('contact/', contact, name='contact'),
]
