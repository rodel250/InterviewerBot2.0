import ctypes
import base64
from tkinter import messagebox as tkMessageBox
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
from django.core.mail import send_mail
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
            q11 = request.POST.get("qtn11")
            q12 = request.POST.get("qtn12")
            q13 = request.POST.get("qtn13")
            q14 = request.POST.get("qtn14")
            q15 = request.POST.get("qtn15")
            q16 = request.POST.get("qtn16")
            q17 = request.POST.get("qtn17")
            q18 = request.POST.get("qtn18")
            q19 = request.POST.get("qtn19")
            q20 = request.POST.get("qtn20")
            r1 = request.POST.get("req1")
            r2 = request.POST.get("req2")
            r3 = request.POST.get("req3")
            r4 = request.POST.get("req4")
            r5 = request.POST.get("req5")
            r6 = request.POST.get("req6")
            r7 = request.POST.get("req7")
            r8 = request.POST.get("req8")
            r9 = request.POST.get("req9")
            r10 = request.POST.get("req10")

            if r1 == "":
                r1 = None

            if r2 == "":
                r2 = None

            if r3 == "":
                r3 = None

            if r4 == "":
                r4 = None
            if r5 == "":
                r5 = None

            if r6 == "":
                r6 = None

            if r7 == "":
                r7 = None

            if r8 == "":
                r8 = None

            if r9 == "":
                r9 = None

            if r10 == "":
                r10 = None

            form = CreateJob(title = jobTitle, description = jobDescription,
                question_11 = q11, question_12 = q12, question_13 = q13, question_14 = q14,
                question_15 = q15, question_16 = q16, question_17 = q17, question_18 = q18,
                question_19 = q19, question_20 = q20, requirement1 = r1, requirement2 = r2,
                requirement3 = r3, requirement4 = r4, requirement5 = r5, requirement6 = r6,
                requirement7 = r7, requirement8 = r8, requirement9 = r9, requirement10 = r10,
                admin_id = currentUser)
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
                    q11 = request.POST.get("qtn11")
                    q12 = request.POST.get("qtn12")
                    q13 = request.POST.get("qtn13")
                    q14 = request.POST.get("qtn14")
                    q15 = request.POST.get("qtn15")
                    q16 = request.POST.get("qtn16")
                    q17 = request.POST.get("qtn17")
                    q18 = request.POST.get("qtn18")
                    q19 = request.POST.get("qtn19")
                    q20 = request.POST.get("qtn20")
                    r1 = request.POST.get("req1")
                    r2 = request.POST.get("req2")
                    r3 = request.POST.get("req3")
                    r4 = request.POST.get("req4")
                    r5 = request.POST.get("req5")
                    r6 = request.POST.get("req6")
                    r7 = request.POST.get("req7")
                    r8 = request.POST.get("req8")
                    r9 = request.POST.get("req9")
                    r10 = request.POST.get("req10")

                    if r1 == "":
                        r1 = None

                    if r2 == "":
                        r2 = None

                    if r3 == "":
                        r3 = None

                    if r4 == "":
                        r4 = None
                    if r5 == "":
                        r5 = None

                    if r6 == "":
                        r6 = None

                    if r7 == "":
                        r7 = None

                    if r8 == "":
                        r8 = None

                    if r9 == "":
                        r9 = None

                    if r10 == "":
                        r10 = None

                    form = CreateJob(title = jobTitle, description = jobDescription,
                        question_11 = q11, question_12 = q12, question_13 = q13, question_14 = q14,
                        question_15 = q15, question_16 = q16, question_17 = q17, question_18 = q18,
                        question_19 = q19, question_20 = q20, requirement1 = r1, requirement2 = r2,
                        requirement3 = r3, requirement4 = r4, requirement5 = r5, requirement6 = r6,
                        requirement7 = r7, requirement8 = r8, requirement9 = r9, requirement10 = r10,
                        admin_id = currentUser)
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
        form = AdministratorForm(request.POST)
        form.first = request.POST.get("first")
        form.last = request.POST.get("last")
        form.phone = request.POST.get("phone")
        form.passwd = request.POST.get("pass")
        form.gender = request.POST.get("gender")
        form.email = request.POST.get("email")

        administrators = Administrator.objects.all()
        count = 0

        for administrator in administrators:
            if(administrator.emailAddress == form.email):
                count = 1

        if (count == 0):
            if password_check(form.passwd, request):
                if(form.is_valid()):
                    fname = request.POST.get("first")
                    lname = request.POST.get("last")
                    phone = request.POST.get("phone")
                    password = request.POST.get("pass")
                    gender = request.POST.get("gender")
                    emailAdd = request.POST.get("email")
                    email = emailAdd

                    password = encrypt_password(password)

                    form = Administrator(firstname = fname, lastname = lname, phone = phone, password = password, gender = gender, 
                                            emailAddress = emailAdd)
                    form.save()

                    send_mail(
                        'Your Registration was Successful.',
                        'Thank you for registering! You may login now using your newly created account.',
                        'email',
                        [email],
                        fail_silently=False,
                    )

                    messages.success(request, 'Account created for '+email)
                    return redirect('user:login_view')
        else:
            messages.error(request, 'Email address is already taken.')
        
        return render(request, 'registeradmin.html', {'form':form})

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

        if 'btnAdd' in request.POST:
            if form.is_valid():
                jobTitle = request.POST.get("name-title")
                jobDescription = request.POST.get("name-description")
                q11 = request.POST.get("qtn11")
                q12 = request.POST.get("qtn12")
                q13 = request.POST.get("qtn13")
                q14 = request.POST.get("qtn14")
                q15 = request.POST.get("qtn15")
                q16 = request.POST.get("qtn16")
                q17 = request.POST.get("qtn17")
                q18 = request.POST.get("qtn18")
                q19 = request.POST.get("qtn19")
                q20 = request.POST.get("qtn20")
                r1 = request.POST.get("req1")
                r2 = request.POST.get("req2")
                r3 = request.POST.get("req3")
                r4 = request.POST.get("req4")
                r5 = request.POST.get("req5")
                r6 = request.POST.get("req6")
                r7 = request.POST.get("req7")
                r8 = request.POST.get("req8")
                r9 = request.POST.get("req9")
                r10 = request.POST.get("req10")

                if r1 == "":
                    r1 = None

                if r2 == "":
                    r2 = None

                if r3 == "":
                    r3 = None

                if r4 == "":
                    r4 = None
                if r5 == "":
                    r5 = None

                if r6 == "":
                    r6 = None

                if r7 == "":
                    r7 = None

                if r8 == "":
                    r8 = None

                if r9 == "":
                    r9 = None

                if r10 == "":
                    r10 = None

                form = CreateJob(title = jobTitle, description = jobDescription,
                    question_11 = q11, question_12 = q12, question_13 = q13, question_14 = q14,
                    question_15 = q15, question_16 = q16, question_17 = q17, question_18 = q18,
                    question_19 = q19, question_20 = q20, requirement1 = r1, requirement2 = r2,
                    requirement3 = r3, requirement4 = r4, requirement5 = r5, requirement6 = r6,
                    requirement7 = r7, requirement8 = r8, requirement9 = r9, requirement10 = r10,
                    admin_id = currentUser)
                form.save()
                return redirect('administrator:job-lists_view')

        elif 'btnUpdate' in request.POST:
            administrator_id = request.POST.get("administrator-id")
            firstName = request.POST.get("firstname")
            lastName = request.POST.get("lastname")
            phone = request.POST.get("phone")
            password = request.POST.get("password")

            if password == "":
                update_administrator = Administrator.objects.filter(id = administrator_id).update(firstname = firstName,
                    lastname = lastName, phone = phone)
                messages.success(request, 'Profile Successfully Updated')
            elif password_check(password, request):
                password = encrypt_password(password)
                update_administrator = Administrator.objects.filter(id = administrator_id).update(firstname = firstName,
                    lastname = lastName, phone = phone, password = password)
                messages.success(request, 'Profile Successfully Updated')

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

class LogOutView(View):
    def get(self, request):
        return render(request, 'LogOut.html')