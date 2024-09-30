from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users.models import Contact
from users.models import Join_us
from users.models import Book
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.contrib import messages
from django.core.mail import EmailMessage

import os
from uuid import uuid4

from main.decorators import user_is_superuser
from .forms import NewsletterForm
from users.models import SubscribedUsers


# from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request, 'index.html')




# def ourteam(request):
#     return render(request, "our team.html")

def about(request):
    return render(request, "about.html")




def contact(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(firstname=firstname,lastname=lastname, email=email, subject=subject, message=message, date= datetime.today())
        contact.save()
        
        send_mail(
            "Assistance with Login, Password Reset, Donations, and Book Purchases",
            f"Dear {firstname},\n",
            "sainath.girme88@gmail.com",
            [email],
            fail_silently=False,
        )
    return render(request, "contact.html")


