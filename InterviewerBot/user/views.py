from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
from django.core.files.storage import default_storage
from django.core.mail import send_mail
# Create your views here.

class UserIndexView(View):
	def get(self, request):
		return render(request, 'UserLog-inPage.html')

	def post(self, request):
		email = request.POST.get("emailAdd")
		password = request.POST.get("pass")
		applicants = Applicant.objects.all()
		form = LoginForm(request.POST)

		for applicant in applicants:
			if(applicant.emailAddress == email and applicant.password == password):
				if(form.is_valid()):
					form = Login.objects.get(id=1)
					form.emailAddress = email
					form.password = password
					form.save()
				return redirect('user:home_view')

		return HttpResponse('Email address or password is incorrect.')

class AboutUsView(View):
	def get(self, request):
		return render(request, 'AboutUs.html')

class ContactUsView(View):
	def get(self, request):
		return render(request, 'ContactUs.html')

	def post(self, request):
		form = ContactForm(request.POST)
		if form.is_valid():
			email = request.POST.get("email")
			subject = request.POST.get("subject")
			message = request.POST.get("message")
			send_mail(subject,message,email,['interviewbot.cit@gmail.com',email])

			return redirect('user:contact-us_view')

		return render(request, 'ContactUs.html')
					

class HomePageView(View):
	def get(self, request):
		return render(request, 'homePage.html')

class JobInterviewView(View):
	def get(self, request):
		return render(request, 'jobOffer_Interview.html')

class SettingsView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("emailAddress", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(emailAddress = currentUser)

		context = {
			'applicant': applicant
		}

		return render(request, 'Settings.html', context)

	def post(self, request):
		form = UpdateForm(request.POST)
		currentUser = Login.objects.values_list("emailAddress", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(emailAddress = currentUser)

		firstName = request.POST.get("firstname")
		lastName = request.POST.get("lastname")
		phone = request.POST.get("phone")
		email = request.POST.get("email")
		password = request.POST.get("password")

		if(form.is_valid):
			update_applicant = Applicant.objects.filter(emailAddress=email).update(firstname = firstName,
				lastname = lastName, phone = phone, emailAddress = email, password = password)

		return redirect('user:settings_view')

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

				return redirect('user:login_view')
		else:
			print(form.errors)
			return HttpResponse('Email address is already used.')
		
		return HttpResponse('not valid')

class JobOffersView(View):
	def get(self, request):
		return render(request, 'jobOffers.html')