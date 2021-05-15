import ctypes
import base64
import os

import speech_recognition as sr
from gtts import gTTS

from .forms import *
from .models import *
from administrator.models import Administrator
from administrator.models import CreateJob
from administrator.models import currentJob

from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse

from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.

def Mbox(title, text, style):
	sty=int(style)+4096
	return ctypes.windll.user32.MessageBoxW(0, title, text, sty)

def encrypt_password(password):
	password_bytes = password.encode('ascii')
	base64_bytes = base64.b64encode(password_bytes)
	password = base64_bytes.decode('ascii')

	return password

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

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

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
						email = emailAddress

						password = encrypt_password(password)

						form = Applicant(firstname = firstname, lastname = lastname, phone = phone, password = password, gender = gender, emailAddress = emailAddress)
						form.save()

						send_mail(
						    'Your Registration was Successful.',
						    'Thank you for registering! You may login now using your newly created account.',
						    'email',
						    [email],
						    fail_silently=False,
						)

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

			password = encrypt_password(password)

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

		if password == "":
			update_applicant = Applicant.objects.filter(id = applicant_id).update(firstname = firstName,
				lastname = lastName, phone = phone)
			Mbox('Profile Update Successful', 'Success', 64)
		elif password_check(password, request):
			password = encrypt_password(password)
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

				saved_jobs = SavedJobs.objects.filter(user_id = user_id)

				for saved_job in saved_jobs:
					count = count + 1

				if count < 5:
					save_jobs = SavedJobs.objects.create(job_id = job_id, user_id = user_id)
				else:
					Mbox('Email address is already taken.', 'Error', 16)
				return redirect('user:job-offers_view')
			# elif 'btnApply' in request.POST:
				
class LogOutView(View):
	def get(self, request):
		return render(request, 'LogOut.html')

class MailSentView(View):
	def get(self, request):
		return render(request, 'MailSent.html')

class JobInterviewView(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}

		for job in job:
			tts1 = gTTS(text=job.question_1, lang="en")
			tts1.save("%s.mp3" % os.path.join('user/static/questions', 'question1'))

			tts2 = gTTS(text=job.question_2, lang="en")
			tts2.save("%s.mp3" % os.path.join('user/static/questions', 'question2'))

			tts3 = gTTS(text=job.question_3, lang="en")
			tts3.save("%s.mp3" % os.path.join('user/static/questions', 'question3'))

			tts4 = gTTS(text=job.question_4, lang="en")
			tts4.save("%s.mp3" % os.path.join('user/static/questions', 'question4'))

			tts5 = gTTS(text=job.question_5, lang="en")
			tts5.save("%s.mp3" % os.path.join('user/static/questions', 'question5'))

			# tts4 = gTTS(text=job.question_6, lang="en")
			# tts4.save("%s.mp3" % os.path.join('user/static/questions', 'question6'))

			# tts4 = gTTS(text=job.question_7, lang="en")
			# tts4.save("%s.mp3" % os.path.join('user/static/questions', 'question7'))

			# tts4 = gTTS(text=job.question_8, lang="en")
			# tts4.save("%s.mp3" % os.path.join('user/static/questions', 'question8'))

			# tts9 = gTTS(text=job.question_9, lang="en")
			# tts9.save("%s.mp3" % os.path.join('user/static/questions', 'question9'))

			# tts10 = gTTS(text=job.question_10, lang="en")
			# tts10.save("%s.mp3" % os.path.join('user/static/questions', 'question10'))

		return render(request, 'jobOffer_Interview.html', context)

class JobInterviewQ1View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}

		return render(request, 'jobInterview_Q1.html', context)

class JobInterviewQ2View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}

		return render(request, 'jobInterview_Q2.html', context)

class JobInterviewQ3View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}

		return render(request, 'jobInterview_Q3.html', context)

class JobInterviewQ4View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}

		return render(request, 'jobInterview_Q4.html', context)

class JobInterviewQ5View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}

		return render(request, 'jobInterview_Q5.html', context)