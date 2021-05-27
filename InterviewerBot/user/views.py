import ctypes
import base64
import os
# import speech_recognition as sr
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

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError


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

						messages.success(request, "Account created for "+email)
						return redirect('user:login_view')
			else:
				messages.error(request, "Email address is already taken.")
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
			'appliedjobs': appliedjobs,
		}

		return render(request, 'homePage.html', context)

	def post(self, request):
		if request.method == "POST":
			if 'btnUnsave' in request.POST:
				currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
				applicant = Applicant.objects.filter(id = currentUser)

				job_id = request.POST.get("job-id")
				savedjobs = SavedJobs.objects.filter(job_id = job_id).delete()

				return redirect('user:home_view')
			elif 'btnApply' in request.POST:
				user_id = request.POST.get("user-id")
				job_id = request.POST.get("job-id")
				job = currentJob.objects.filter(id = 1).update(jobID = job_id)
				savedjobs = SavedJobs.objects.filter(job_id = job_id).delete()

				try:
					r1 = request.FILES['myfile1']
				except MultiValueDictKeyError:
					r1 = None

				try:
					r2 = request.FILES['myfile2']
				except MultiValueDictKeyError:
					r2 = None

				try:
					r3 = request.FILES['myfile3']
				except MultiValueDictKeyError:
					r3 = None

				try:
					r4 = request.FILES['myfile4']
				except MultiValueDictKeyError:
					r4 = None

				try:
					r5 = request.FILES['myfile5']
				except MultiValueDictKeyError:
					r5 = None

				try:
					r6 = request.FILES['myfile6']
				except MultiValueDictKeyError:
					r6 = None

				try:
					r7 = request.FILES['myfile7']
				except MultiValueDictKeyError:
					r7 = None

				try:
					r8 = request.FILES['myfile8']
				except MultiValueDictKeyError:
					r8 = None

				try:
					r9 = request.FILES['myfile9']
				except MultiValueDictKeyError:
					r9 = None

				try:
					r10 = request.FILES['myfile10']
				except MultiValueDictKeyError:
					r10 = None

				apply_job = AppliedJob(requirement_1 = r1, requirement_2 = r2, requirement_3 = r3, 
					requirement_4 = r4, requirement_5 = r5, requirement_6 = r6, requirement_7 = r7, 
					requirement_8 = r8, requirement_9 = r9, requirement_10 = r10, job_id = job_id, 
					user_id = user_id)
				apply_job.save()

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

		if password == "":
			update_applicant = Applicant.objects.filter(id = applicant_id).update(firstname = firstName,
				lastname = lastName, phone = phone)
		elif password_check(password, request):
			password = encrypt_password(password)
			update_applicant = Applicant.objects.filter(id = applicant_id).update(firstname = firstName,
				lastname = lastName, phone = phone, password = password)

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
					Mbox('You can only save at most 5 job offers.', 'Error', 16)
				return redirect('user:job-offers_view')
			elif 'btnApply' in request.POST:
				context = {}
				user_id = request.POST.get("user-id")
				job_id = request.POST.get("job-id")
				job = currentJob.objects.filter(id = 1).update(jobID = job_id)

				# To store the files in the media dir
				fs = FileSystemStorage();
				try:
					r1 = request.FILES['myfile1']
					fs.save(r1.name, r1)
				except MultiValueDictKeyError:
					r1 = None

				try:
					r2 = request.FILES['myfile2']
					fs.save(r2.name, r2)
				except MultiValueDictKeyError:
					r2 = None

				try:
					r3 = request.FILES['myfile3']
					fs.save(r3.name, r3)
				except MultiValueDictKeyError:
					r3 = None

				try:
					r4 = request.FILES['myfile4']
					fs.save(r4.name, r4)
				except MultiValueDictKeyError:
					r4 = None

				try:
					r5 = request.FILES['myfile5']
					fs.save(r5.name, r5)
				except MultiValueDictKeyError:
					r5 = None

				try:
					r6 = request.FILES['myfile6']
					fs.save(r6.name, r6)
				except MultiValueDictKeyError:
					r6 = None

				try:
					r7 = request.FILES['myfile7']
					fs.save(r7.name, r7)
				except MultiValueDictKeyError:
					r7 = None

				try:
					r8 = request.FILES['myfile8']
					fs.save(r8.name, r8)
				except MultiValueDictKeyError:
					r8 = None

				try:
					r9 = request.FILES['myfile9']
					fs.save(r9.name, r9)
				except MultiValueDictKeyError:
					r9 = None

				try:
					r10 = request.FILES['myfile10']
					fs.save(r10.name, r10)
				except MultiValueDictKeyError:
					r10 = None

				apply_job = AppliedJob(requirement_1 = r1, requirement_2 = r2, requirement_3 = r3, 
					requirement_4 = r4, requirement_5 = r5, requirement_6 = r6, requirement_7 = r7, 
					requirement_8 = r8, requirement_9 = r9, requirement_10 = r10, job_id = job_id, 
					user_id = user_id)
				apply_job.save()

				return redirect('user:job-interview_view')
				
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

		# for job in job:
		# 	tts1 = gTTS(text=job.question_1, lang="en")
		# 	tts1.save("%s.mp3" % os.path.join('user/static/questions', 'question1'))

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

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_1 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_1 = response_1)
		return redirect('user:job-interview_q2')

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

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_2 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_2 = response_2)
		return redirect('user:job-interview_q3')

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

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_3 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_3 = response_3)
		return redirect('user:job-interview_q4')

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

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_4 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_4 = response_4)
		return redirect('user:job-interview_q5')

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

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_5 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_5 = response_5)
		return redirect('user:job-interview_q6')

class JobInterviewQ6View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q6.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_6 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_6 = response_6)
		return redirect('user:job-interview_q7')

class JobInterviewQ7View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q7.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_7 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_7 = response_7)
		return redirect('user:job-interview_q8')

class JobInterviewQ8View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q8.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_8 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_8 = response_8)
		return redirect('user:job-interview_q9')

class JobInterviewQ9View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q9.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_9 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_9 = response_9)
		return redirect('user:job-interview_q10')

class JobInterviewQ10View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q10.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_10 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_10 = response_10)
		return redirect('user:job-interview_q11')

class JobInterviewQ11View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q11.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_11 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_11 = response_11)
		return redirect('user:job-interview_q12')

class JobInterviewQ12View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q12.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_12 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_12 = response_12)
		return redirect('user:job-interview_q13')

class JobInterviewQ13View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q13.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_13 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_13 = response_13)
		return redirect('user:job-interview_q14')

class JobInterviewQ14View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q14.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_14 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_14 = response_14)
		return redirect('user:job-interview_q15')

class JobInterviewQ15View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q15.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_15 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_15 = response_15)
		return redirect('user:job-interview_q16')

class JobInterviewQ16View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q16.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_16 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_16 = response_16)
		return redirect('user:job-interview_q17')

class JobInterviewQ17View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q17.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_17 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_17 = response_17)
		return redirect('user:job-interview_q18')

class JobInterviewQ18View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q18.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_18 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_18 = response_18)
		return redirect('user:job-interview_q19')

class JobInterviewQ19View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q19.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_19 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_19 = response_19)
		return redirect('user:job-interview_q20')

class JobInterviewQ20View(View):
	def get(self, request):
		currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		applicant = Applicant.objects.filter(id = currentUser)
		interview_job = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)
		job = CreateJob.objects.filter(id = interview_job)

		context = {
			'applicant': applicant,
			'job': job
		}
		return render(request, 'jobInterview_Q20.html', context)

	def post(self, request):
		user = Login.objects.values_list("user_id", flat=True).get(pk = 1)
		job = currentJob.objects.values_list("jobID", flat=True).get(pk=1)
		response_20 = request.POST.get("message")
		update_applyJob = AppliedJob.objects.filter(job_id = job, user_id = user).update(response_20 = response_20)
		return redirect('user:interview_success_view')

class InterviewSuccessView(View):
	def get(self, request):
		return render(request, 'interviewSuccess.html')