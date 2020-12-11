import ctypes
from tkinter import messagebox as tkMessageBox
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
from administrator.models import Administrator
from administrator.models import CreateJob
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.core.paginator import Paginator

# Create your views here.

def Mbox(title, text, style):
	return ctypes.windll.user32.MessageBoxW(0, title, text, style)

def password_check(password):
	specialSymbols = ['$', '*', '#', '@', '%', '!', '^', '&']
	val = True

	if len(password) < 6: 
		Mbox('length should be at least 6', 'Error', 16) 
		val = False

	if len(password) > 20:
		Mbox('length should be not be greater than 8', 'Error', 16) 
		val = False  

	if not any(char.isdigit() for char in password): 
		Mbox('Password should have at least one numeral', 'Error', 16) 
		val = False

	if not any(char.isupper() for char in password): 
		Mbox('Password should have at least one uppercase letter', 'Error', 16) 
		val = False

	if not any(char.islower() for char in password): 
		Mbox('Password should have at least one lowercase letter', 'Error', 16) 
		val = False

	if not any(char in specialSymbols for char in password): 
		Mbox('Password should have at least one of the symbols $@#*@%!^&', 'Error', 16) 
		val = False

	if val:
		return val

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
					Mbox('WELCOME '+applicant.firstname, 'Success', 64)
				return redirect('user:home_view')

		for administrator in administrators:
			if (administrator.emailAddress == email and administrator.password == password):
				if (form.is_valid()):
					form = Login.objects.get(id=1)
					form.user_id = administrator.id
					form.emailAddress = email
					form.password = password
					form.save()
					Mbox('WELCOME '+administrator.firstname, 'Success', 64)
				return redirect('administrator:dashboard_view')

		Mbox('Email address or password is inccorect', 'Error', 16)
		return redirect('user:login_view')

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

		context = {
			'applicant': applicant,
			'savedjobs': savedjobs,
		}

		return render(request, 'homePage.html', context)

	def post(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)

		job_id = request.POST.get("job-id")
		savedjobs = SavedJobs.objects.filter(job_id = job_id).delete()

		return redirect('user:home_view')

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

		if password_check(password):
			update_applicant = Applicant.objects.filter(id = applicant_id).update(firstname = firstName,
				lastname = lastName, phone = phone, password = password)
			Mbox('Profile Update Successful', 'Success', 64)

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
				
				if password_check(password):
					form = Applicant(firstname = fname, lastname = lname, phone = phone, password = password, gender = gender, 
											emailAddress = emailAdd)
					form.save()
					Mbox('Successfully Registered', 'Success', 64)

					return redirect('user:login_view')
		else:
			print(form.errors)
			return HttpResponse('Email address is already used.')
		
		Mbox('Registration failed', 'Error', 16) 
		return redirect('user:registration_view')

class JobOffersView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		joblists = CreateJob.objects.raw('SELECT createjob.id, createjob.title, createjob.description FROM createjob WHERE createjob.id NOT IN (SELECT savedjobs.job_id FROM savedjobs, currentuser WHERE currentuser.user_id = savedjobs.user_id)')

		# p = Paginator(joblists,3)
		# page_number = request.GET.get('page',1)
		# page = p.page(page_number)
		# numberOfPage = p.num_pages

		# array = []
		# for x in range(1, numberOfPage+1):
		# 	array.append(x)

		context = {
			'applicant': applicant,
			'joblists': joblists,
			# 'joblists': page,
			# 'pages': array,
			# 'page_number': int(page_number)
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

				saved_jobs = SavedJobs.objects.all()

				for saved_job in saved_jobs:
					count = count + 1

				if count < 5:
					save_jobs = SavedJobs.objects.create(job_id = job_id, user_id = user_id, job_header = job_title, job_description = job_description)
					return redirect('user:job-offers_view')
			# elif 'btnSearch' in request.POST:
			# 	searchData = request.POST.get("search")
			# 	searchData = searchData.split()
			# 	print(searchData)
			# 	joblists = CreateJob.objects.raw('SELECT createjob.id, createjob.title, createjob.description FROM createjob WHERE createjob.title = %s AND createjob.id NOT IN (SELECT savedjobs.job_id FROM savedjobs, currentuser WHERE currentuser.user_id = savedjobs.user_id)', [searchData])

			# 	context = {
			# 		'joblists': joblists,
			# 	}

			# 	return render(request, 'jobOffers.html', context)

		return HttpResponse('You can only save at most 5 job offerings.')

class LogOutView(View):
	def get(self, request):
		return render(request, 'LogOut.html')

class MailSentView(View):
	def get(self, request):
		return render(request, 'MailSent.html')
