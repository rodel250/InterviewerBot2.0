from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
# from django.http import Http404
# from django.http import HttpResponse
# from .forms import *
# from .models import *
from django.core.files.storage import default_storage
# Create your views here.

class UserIndexView(View):
	def get(self, request):
		return render(request, 'UserLog-inPage.html')

class AboutUsView(View):
	def get(self, request):
		return render(request, 'AboutUs.html')

class ContactUsView(View):
	def get(self, request):
		return render(request, 'ContactUs.html')

class HomePageView(View):
	def get(self, request):
		return render(request, 'homePage.html')

class JobInterviewView(View):
	def get(self, request):
		return render(request, 'jobOffer_Inteview.html')

class UserRegistrationView(View):
	def get(self, request):
		return render(request, 'RegistrationPage.html')

class JobOffersView(View):
	def get(self, request):
		return render(request, 'jobOffers.html')