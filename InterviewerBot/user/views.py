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

class UserRegistrationView(View):
	def get(self, request):
		return render(request, 'RegistrationPage.html')

	def post(self, request):
		form = ApplicantForm(request.POST)

		if(form.is_valid()):
			fname = request.POST.get("firstname")
			lname = request.POST.get("lastname")
			password = request.POST.get("password")
			gender = request.POST.get("gender")
			emailAdd = request.POST.get("emailAddress")

			form = Applicant(firstname = fname, lastname = lname, password = password, gender = gender, 
								emailAddress = emailAdd)
			form.save()

			return redirect('user:login_view')
		else:
			print(form.errors)
			return HttpResponse('not valid')

class JobOffersView(View):
	def get(self, request):
		return render(request, 'jobOffers.html')