from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
from user.models import Login
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
# Create your views here.

class CreateJobView(View):
    def get(self, request):
        return render(request, 'createJob.html')

class DashboardView(View):
    def get(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        administrator = Administrator.objects.filter(id = currentUser)

        context = {
            'administrator': administrator
        }
        return render(request, 'admindashboard.html', context)

    def post(self, request):
        form = CreateJobForm(request.POST)

        if(form.is_valid()):
            jobTitle = request.POST.get("title")
            jobDescription = request.POST.get("description")
            jobQuestion = request.POST.get("question")
            jobAnswer = request.POST.get("answer")

            form = CreateJob(title = jobTitle, description = jobDescription, question = jobQuestion,
                                    answer = jobAnswer)
            form.save()

            return redirect('administrator:dashboard_view')
        else:
            print(form.errors)
            return HttpResponse('not valid')

class JobListsView(View):
    def get(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        administrator = Administrator.objects.filter(id = currentUser)
        joblist = Joblist.objects.all()

        p = Paginator(joblist,2)
        page_number = request.GET.get('page',1)
        page = p.page(page_number)
        numberOfPage = p.num_pages
        

        array = []
        for x in range(1, numberOfPage+1):
            array.append(x)
            

        context = {
            'administrator': administrator,
            'joblists': page,
            'pages':array,
            'page_number':int(page_number)

        }

        return render(request, 'adminjoblist.html', context)

    def post(self, request):
        if request.method == 'POST':
            if 'btnDelete' in request.POST:
                jobID1 = request.POST.get("jobID")
                job = Joblist.objects.filter(id=jobID1).delete()
            
            elif 'btnUpdate' in request.POST:
                jobID1 = request.POST.get("jobID")
                jobDesription1 = request.POST.get("jobDescription")
                jobHeader1 = request.POST.get("jobHeader")
                job = Joblist.objects.filter(id=jobID1).update(job_description = jobDesription1, job_header= jobHeader1)
    
        return redirect('administrator:job-lists_view')
        
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

class SettingsView(View):
    def get(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        administrator = Administrator.objects.filter(id = currentUser)

        context = {
            'administrator': administrator
        }

        return render(request, 'adminsettings.html', context)

    def post(self, request):
        administrator = Administrator.objects.all()
        count = 1

        administrator_id = request.POST.get("administrator-id")
        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        update_administrator = Administrator.objects.filter(id = administrator_id).update(firstname = firstName,
            lastname = lastName, phone = phone, password = password)

        return redirect('administrator:settings_view')