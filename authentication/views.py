from django.shortcuts import render
from django.views import generic


class LoginView(generic.TemplateView):
    template_name = "authentication/login.html"


class RegistrationView(generic.TemplateView):
    template_name = "authentication/registration.html"
