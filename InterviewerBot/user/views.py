from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
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
		return render(request, 'jobOffer_Interview.html')

class SettingsView(View):
	def get(self, request):
		return render(request, 'Settings.html')

class UserRegistrationView(View):
	def get(self, request):
		return render(request, 'RegistrationPage.html')

	def post(self, request):
		count = 0
		form = ApplicantForm(request.POST)
		applicants = Applicant.objects.all()
		emailAdd = request.POST.get("email")

		for applicant in applicants:
			if(applicant.emailAddress == emailAdd):
				count = 1

		if (count == 0):
			if(form.is_valid()):
				fname = request.POST.get("first")
				lname = request.POST.get("last")
				phone = request.POST.get("phone")
				password = request.POST.get("pass")
				gender = request.POST.get("gender")
				emailAdd = request.POST.get("email")

				form = Applicant(firstname = fname, lastname = lname, phone = phone, password = password, gender = gender, 
										emailAddress = emailAdd)
				form.save()

				return redirect('user:login')
		else:
			print(form.errors)
			return HttpResponse('Email address is already used.')
		
		return HttpResponse('not valid')

class JobOffersView(View):
	def get(self, request):
		return render(request, 'jobOffers.html')