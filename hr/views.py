from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from hr.models import JobPost, CandidateApplications, SelectCandidateJob, JobApply
from hr.decorators import is_hr, hr_required

@hr_required
def hrHome(request):
    if is_hr(request.user):
        jobposts = JobPost.objects.filter(user=request.user)
        return render(request, 'hr/hrdash.html', {'jobposts': jobposts})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('homepage')

@hr_required
def hrCandidateDetails(request, id):
    if JobPost.objects.filter(id=id).exists():
        jobpost = JobPost.objects.get(id=id)
        jobapplys = CandidateApplications.objects.filter(job=jobpost)
        selectedCandidate = SelectCandidateJob.objects.filter(job=jobpost)
        return render(request, 'hr/candidate.html', {'jobapplys': jobapplys, 'jobpost': jobpost, 'selectedCandidate': selectedCandidate})
    else:
        messages.error(request, "Job post not found.")
        return redirect('hrdash')

@user_passes_test(is_hr)
def postJobs(request):
    if request.method == 'POST':
        job_title = request.POST.get('job-title')
        address = request.POST.get('address')
        company_name = request.POST.get('company-name')
        salary_low = request.POST.get('salary-low')
        salary_high = request.POST.get('salary-high')
        last_date = request.POST.get('last-date')

        jobpost = JobPost(
            user=request.user, 
            title=job_title, 
            address=address, 
            companyName=company_name, 
            salaryLow=salary_low, 
            salaryHigh=salary_high, 
            lastDateToApply=last_date
        )
        jobpost.save()
        messages.success(request, "Job successfully posted.")
        return render(request, 'hr/postjob.html')
    return render(request, 'hr/postjob.html')

def acceptApplication(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid') 
        candidate = CandidateApplications.objects.get(id=candidateid)
        candidate.status = 'Accepted'  # Modify the status field
        candidate.save()

        jobpost = JobPost.objects.get(id=jobpostid)
        if not SelectCandidateJob.objects.filter(candidate=candidate).exists():
            SelectCandidateJob(job=jobpost, candidate=candidate).save()

        # Send acceptance email
        subject = 'Job Application Accepted'
        message = f'Dear {candidate.user.username},\n\nCongratulations! Your application has been accepted. Please visit the company for next procedure. Thank You!'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [candidate.user.email])

        messages.success(request, 'Candidate accepted and email sent.')
        return redirect(f'/candidatedetails/{jobpostid}/')
    return redirect('hrdash')

def rejectApplication(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('candidateid')
        candidate = JobApply.objects.get(id=candidate_id)
        candidate.status = "Rejected"
        candidate.save()

        # Send rejection email
        subject = 'Job Application Status'
        message = f'Dear {candidate.user.username},\n\nYour application has been rejected. Thank you for applying.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [candidate.user.email])

        messages.success(request, 'Candidate rejected and email sent.')
        return redirect('hrdash')
    return redirect('hrdash')
