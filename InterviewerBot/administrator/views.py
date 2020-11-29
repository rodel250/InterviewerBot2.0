from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
# from django.http import Http404
# from django.http import HttpResponse
# from .forms import *
# from .models import *
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