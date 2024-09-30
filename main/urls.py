from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("About", views.about, name="Helping Hands About"),
    path("Contact", views.contact, name="contact"),
    

]