from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
from django.core.files.storage import default_storage
# Create your views here.

class CreateJobView(View):
	def get(self, request):
		return render(request, 'createJob.html')

class DashboardView(View):
	def get(self, request):
		return render(request, 'admindashboard.html')

class JobListsView(View):
	def get(self, request):
		return render(request, 'adminjoblist.html')

class AdminRegistrationView(View):
	def get(self, request):
		return render(request, 'registeradmin.html')

	def post(self, request):
		count = 0
		form = AdministratorForm(request.POST)
		administrators = Administrator.objects.all()
		emailAdd = request.POST.get("email")

		for administrator in administrators:
			if(administrator.emailAddress == emailAdd):
				count = 1

		if (count == 0):
			if(form.is_valid()):
				fname = request.POST.get("first")
				lname = request.POST.get("last")
				phone = request.POST.get("phone")
				password = request.POST.get("pass")
				gender = request.POST.get("gender")
				emailAdd = request.POST.get("email")

				form = Administrator(firstname = fname, lastname = lname, phone = phone, password = password, gender = gender, 
										emailAddress = emailAdd)
				form.save()

				return redirect('user:login_view')
		else:
			print(form.errors)
			return HttpResponse('Email address is already used.')
		
		return HttpResponse('not valid')