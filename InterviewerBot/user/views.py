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
from django.contrib import messages

# Create your views here.

def Mbox(title, text, style):
	return ctypes.windll.user32.MessageBoxW(0, title, text, style, 0x1000)

def password_check(password, request):
	specialSymbols = ['$', '*', '#', '@', '!', '&', '.']
	val = True

	if len(password) < 6 or len(password) > 20:
		messages.error(request,'Password should be at least 6 and not greater than 20 characters')
		val = False
	
	if not any(char.isdigit() for char in password): 
		messages.error(request,'Password should have at least one numeral')
		val = False
	
	if not any(char.isupper() for char in password): 
		messages.error(request,'Password should have at least one uppercase letter')
		val = False
					
	if not any(char.islower() for char in password): 
		messages.error(request,'Password should have at least one lowercase letter')
		val = False
	
	if not any(char in specialSymbols for char in password): 
		messages.error(request,'Password should have at least one of the symbols $#*!&@.')
		val = False

	if val:
		return val

class UserRegistrationView(View):
	def get(self, request):
		return render(request, 'RegistrationPage.html')

	def post(self, request):
		if request.method == 'POST':
			form = ApplicantForm(request.POST)
			form.first = request.POST.get("firstName")
			form.last = request.POST.get("lastName")
			form.phone = request.POST.get("phone")
			form.passwd = request.POST.get("pass")
			form.gender = request.POST.get("gender")
			form.email = request.POST.get("email")

			applicants = Applicant.objects.all()
			count = 0

			for applicant in applicants:
				if(applicant.emailAddress == form.email):
					count = 1

			if (count == 0):
				if password_check(form.passwd, request):
					if(form.is_valid()):
						firstname = request.POST.get("firstName")
						lastname = request.POST.get("lastName")
						phone = request.POST.get("phone")
						password = request.POST.get("pass")
						gender = request.POST.get("gender")
						emailAddress = request.POST.get("email")

						form = Applicant(firstname = firstname, lastname = lastname, phone = phone, password = password, gender = gender, emailAddress = emailAddress)
						form.save()

						Mbox('Successfully Registered', 'Success', 64)
						return redirect('user:login_view')
			else:
				Mbox('Email address is already taken.', 'Error', 16)
		
		return render(request, 'RegistrationPage.html', {'form':form})

class UserIndexView(View):
	def get(self, request):
		return render(request, 'UserLog-inPage.html')

	def post(self, request):
		if request.method == 'POST':
			form = LoginForm(request.POST)
			form.email = request.POST.get("emailAdd")
			email = request.POST.get("emailAdd")
			password = request.POST.get("pass")
			applicants = Applicant.objects.all()
			administrators = Administrator.objects.all()

			for applicant in applicants:
				if(applicant.emailAddress == email and applicant.password == password):
					if(form.is_valid()):
						form = Login.objects.get(id=1)
						form.user_id = applicant.id
						form.emailAddress = email
						form.password = password
						form.save()
						# Mbox('WELCOME '+applicant.firstname, 'Success', 64)
						return redirect('user:home_view')
			
			for administrator in administrators:
				if (administrator.emailAddress == email and administrator.password == password):
					if (form.is_valid()):
						form = Login.objects.get(id=1)
						form.user_id = administrator.id
						form.emailAddress = email
						form.password = password
						form.save()
						# Mbox('WELCOME '+administrator.firstname, 'Success', 64)
						return redirect('administrator:dashboard_view')

		# Mbox('Email address or password is inccorect', 'Error', 16)
		messages.error(request,'email address or password is incorrect')
		return render(request, 'UserLog-inPage.html', {'form':form})

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

			form = Contact(email = email, subject = subject, message = message)
			form.save()
			
			send_mail(subject,message,email,['interviewbot.cit@gmail.com'])

			return redirect('user:mailsent_view')

		return render(request, 'ContactUs.html')
					

class HomePageView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		savedjobs = SavedJobs.objects.raw('SELECT * FROM currentuser, savedjobs, createjob WHERE currentuser.user_id = savedjobs.user_id AND createjob.id = savedjobs.job_id')
		appliedjobs = AppliedJob.objects.raw('SELECT * FROM currentuser, appliedjob, createjob WHERE currentuser.user_id = appliedjob.user_id AND createjob.id = appliedjob.job_id')

		context = {
			'applicant': applicant,
			'savedjobs': savedjobs,
			'appliedjobs': appliedjobs
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
	
	def post(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		if request.method == 'POST':
			print("press")
				# response = request.POST.get("message")
				

				# save = AppliedJob(user_id = currentUser, job_id = 1, response_1 = response , response_2 = "test", response_3 = "test", 
				# response_4 = "test", response_5 = "test", response_6 = "test", response_7 = "test", response_8 = "test", response_9 = "test", 
				# response_10 = "test", requirement_1 = "test", requirement_2 = "test", requirement_3 = "test", requirement_4 = "test", requirement_5 = "test", requirement_6 = "test", 
				# requirement_7 = "test", requirement_8 = "test", requirement_9 = "test", requirement_10 = "test",  )

		return redirect('user:job-interview_view')


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

class JobOffersView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		joblists = CreateJob.objects.raw('SELECT createjob.id, createjob.title, createjob.description FROM createjob WHERE createjob.id NOT IN (SELECT savedjobs.job_id FROM savedjobs, currentuser WHERE currentuser.user_id = savedjobs.user_id UNION ALL SELECT appliedjob.job_id FROM appliedjob, currentuser WHERE appliedjob.user_id = currentuser.user_id)')

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

				saved_jobs = SavedJobs.objects.all()

				for saved_job in saved_jobs:
					count = count + 1

				if count < 5:
					save_jobs = SavedJobs.objects.create(job_id = job_id, user_id = user_id)
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