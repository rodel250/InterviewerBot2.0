from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import Http404
from django.http import HttpResponse
from .forms import *
from .models import *
from user.models import Login
from user.models import AppliedJob
from user.models import Applicant
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
# Create your views here.

class DashboardView(View):
    def get(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        administrator = Administrator.objects.filter(id = currentUser)

        context = {
            'administrator': administrator
        }
        return render(request, 'admindashboard.html', context)

    def post(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        form = CreateJobForm(request.POST)
        joblist = CreateJob.objects.filter(admin_id = currentUser)

        if form.is_valid():
            jobTitle = request.POST.get("name-title")
            jobDescription = request.POST.get("name-description")
            print(jobTitle)
            q1 = request.POST.get("qtn1")
            q2 = request.POST.get("qtn2")
            q3 = request.POST.get("qtn3")
            q4 = request.POST.get("qtn4")
            q5 = request.POST.get("qtn5")
            q6 = request.POST.get("qtn6")
            q7 = request.POST.get("qtn7")
            q8 = request.POST.get("qtn8")
            q9 = request.POST.get("qtn9")
            q10 = request.POST.get("qtn10")

            r1 = request.POST.get("mytext[]") #E LOOP TINGALI NI DI KO KIBAW
            # r1 = request.POST.get("mytext[1]")
            # r1 = request.POST.get("mytext[2]")
            # r1 = request.POST.get("mytext[3]")
            # r1 = request.POST.get("mytext[4]")

            form = CreateJob(title = jobTitle, description = jobDescription, question_1 = q1,
                question_2 = q2, question_3 = q3, question_4 = q4, question_5 = q5, question_6 = q6,
                question_7 = q7, question_8 = q8, question_9 = q9, question_10 = q10,
                requirement1 = r1,  admin_id = currentUser)
            form.save()

            return redirect('administrator:job-lists_view')
        else:
            print(form.errors)
            return HttpResponse('not valid')

class JobListsView(View):      
    def get(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        administrator = Administrator.objects.filter(id = currentUser)
        joblist = CreateJob.objects.filter(admin_id = currentUser)
        # count = AppliedJob.objects.filter
        

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
            'page_number':int(page_number),
            

        }

        return render(request, 'adminjoblist.html', context)
        

    def post(self, request):
        currentUser = Login.objects.values_list("user_id", flat=True).get(pk = 1)
        admin = Administrator.objects.filter(id = currentUser)
        form = CreateJobForm(request.POST)
        if request.method == 'POST':
            if 'btnDelete' in request.POST:
                jobID1 = request.POST.get("jobID")
                job = CreateJob.objects.filter(id=jobID1).delete()
                return redirect('administrator:job-lists_view')
            
            elif 'btnUpdate' in request.POST:
                jobID1 = request.POST.get("jobID")
                jobDesription1 = request.POST.get("jobDescription")
                jobHeader1 = request.POST.get("jobHeader")
                job = CreateJob.objects.filter(id=jobID1).update(description = jobDesription1, title= jobHeader1)
                return redirect('administrator:job-lists_view')
            
            elif 'btnAdd' in request.POST:
                if form.is_valid():
                    jobTitle = request.POST.get("name-title")
                    jobDescription = request.POST.get("name-description")
                    q1 = request.POST.get("qtn1")
                    q2 = request.POST.get("qtn2")
                    q3 = request.POST.get("qtn3")
                    q4 = request.POST.get("qtn4")
                    q5 = request.POST.get("qtn5")
                    q6 = request.POST.get("qtn6")
                    q7 = request.POST.get("qtn7")
                    q8 = request.POST.get("qtn8")
                    q9 = request.POST.get("qtn9")
                    q10 = request.POST.get("qtn10")

                    r1 = request.POST.get("mytext[]") #E LOOP TINGALI NI DI KO KIBAW
                    # r1 = request.POST.get("mytext[1]")
                    # r1 = request.POST.get("mytext[2]")
                    # r1 = request.POST.get("mytext[3]")
                    # r1 = request.POST.get("mytext[4]")

                    form = CreateJob(title = jobTitle, description = jobDescription, question_1 = q1,
                        question_2 = q2, question_3 = q3, question_4 = q4, question_5 = q5, question_6 = q6,
                        question_7 = q7, question_8 = q8, question_9 = q9, question_10 = q10,
                        requirement1 = r1, admin_id = currentUser)
                    form.save()
                    return redirect('administrator:job-lists_view')

            elif 'viewApplicant' in request.POST:
                jobID1 = request.POST.get("jobID1")
                currentJob3 = currentJob.objects.filter(pk=1).update(jobID = jobID1)
                currentJob1 = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)           
                # print(jobID1)
                return redirect('administrator:applicants_view')

        
        
        # else:
        #     print(form.errors)
        #     return HttpResponse('not valid')

        
        
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

class Applicants(View):
    def get(self,request):
        currentJob1 = currentJob.objects.values_list("jobID", flat=True).get(pk = 1)    
        currentApplicant1 = currentApplicant.objects.values_list("applicantID",flat = True).get(pk = 1)
        joblist = CreateJob.objects.filter(id = currentJob1)
        applicant = Applicant.objects.raw('SELECT DISTINCT applicant.id,firstname,lastname FROM applicant,createjob,appliedjob WHERE appliedjob.job_id =' + str(currentJob1) +' AND applicant.id = appliedjob.user_id')
        response = AppliedJob.objects.raw('SELECT * FROM appliedjob,createjob,applicant where appliedjob.job_id = createjob.id and appliedjob.user_id = applicant.id and createjob.id = '+str(currentJob1)+' and applicant.id ='+str(currentApplicant1)+' GROUP BY applicant.firstname')
        context = {
            'joblists': joblist,
            'applicants': applicant,
            'responses': response
            
        }

        return render(request, 'jobApplicants.html', context)

    def post(self,request):
        if request.method == 'POST':
                    if 'btnView' in request.POST:
                        applicantID1 = request.POST.get("applicantID")
                        print(applicantID1)
                        currentApplicant1 = currentApplicant.objects.values_list("applicantID",flat = True).get(pk = 1)
                        currentApplicant2 = currentApplicant.objects.filter(pk=1).update(applicantID = applicantID1)
                        return redirect('administrator:applicants_view')
                        

        return HttpResponse()