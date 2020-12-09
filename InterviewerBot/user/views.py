from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
from administrator.models import Administrator
from administrator.models import Joblist
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
		administrators = Administrator.objects.all()
		form = LoginForm(request.POST)

		for applicant in applicants:
			if(applicant.emailAddress == email and applicant.password == password):
				if(form.is_valid()):
					form = Login.objects.get(id=1)
					form.user_id = applicant.id
					form.emailAddress = email
					form.password = password
					form.save()
				return redirect('user:home_view')

		for administrator in administrators:
			if (administrator.emailAddress == email and administrator.password == password):
				if (form.is_valid()):
					form = Login.objects.get(id=1)
					form.user_id = administrator.id
					form.emailAddress = email
					form.password = password
					form.save()
				return redirect('administrator:dashboard_view')

		return HttpResponse('Email address or password is incorrect.')

class AboutUsView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)

		context = {
			'applicant': applicant
		}

		return render(request, 'AboutUs.html', context)

class ContactUsView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)

		context = {
			'applicant': applicant
		}

		return render(request, 'ContactUs.html', context)

	def post(self, request):
		form = ContactForm(request.POST)
		if form.is_valid():
			email = request.POST.get("email")
			subject = request.POST.get("subject")
			message = request.POST.get("message")
			send_mail(subject,message,email,['interviewbot.cit@gmail.com',email])

			return redirect('user:mailsent_view')

		return render(request, 'ContactUs.html')
					

class HomePageView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		savedjobs = SavedJobs.objects.raw('SELECT * FROM currentuser, savedjobs WHERE currentuser.user_id = savedjobs.user_id')
		totalSavedJobs = SavedJobs.objects.raw('SELECT COUNT(*) FROM savedjobs')

		context = {
			'applicant': applicant,
			'savedjobs': savedjobs,
			'totalSavedJobs': totalSavedJobs,
		}

		return render(request, 'homePage.html', context)

class JobInterviewView(View):
	def get(self, request):
		return render(request, 'jobOffer_Interview.html')

class SettingsView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)

		context = {
			'applicant': applicant
		}

		return render(request, 'Settings.html', context)

	def post(self, request):
		applicants = Applicant.objects.all()
		count = 1

		applicant_id = request.POST.get("applicant-id")
		firstName = request.POST.get("firstname")
		lastName = request.POST.get("lastname")
		phone = request.POST.get("phone")
		password = request.POST.get("password")

		update_applicant = Applicant.objects.filter(id = applicant_id).update(firstname = firstName,
			lastname = lastName, phone = phone, password = password)

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
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		joblists = Joblist.objects.raw('SELECT joblist.id, joblist.job_header, joblist.job_description FROM joblist WHERE joblist.id NOT IN (SELECT savedjobs.job_id FROM savedjobs, currentuser WHERE currentuser.user_id = savedjobs.user_id)')

		context = {
			'applicant': applicant,
			'joblists': joblists
		}

		return render(request, 'jobOffers.html', context)

	def post(self, request):
		if request.method == 'POST':
			if 'btnSave' in request.POST:
				count = 0
				user_id = request.POST.get("user-id")
				job_id = request.POST.get("job-id")
				job_title = request.POST.get("job-header")
				job_description = request.POST.get("job-description")
				print(user_id)

				saved_jobs = SavedJobs.objects.all()

				for saved_job in saved_jobs:
					count = count + 1

				if count <= 5:
					save_jobs = SavedJobs.objects.create(job_id = job_id, user_id = user_id, job_header = job_title, job_description = job_description)
					return redirect('user:job-offers_view')

		return HttpResponse('You can only save at most 5 job offerings.')

class LogOutView(View):
	def get(self, request):
		return render(request, 'LogOut.html')

class MailSentView(View):
	def get(self, request):
		return render(request, 'MailSent.html')
