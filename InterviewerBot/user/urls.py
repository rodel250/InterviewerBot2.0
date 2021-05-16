from django.urls import path
from . import views

#path arranged alphabetically by name
app_name= 'user'
urlpatterns=[
    #path('api/data', views.get_data, name='api-data'),

    #TEST URL
    path('login', views.UserIndexView.as_view(), name="login_view"),
    path('about-us', views.AboutUsView.as_view(), name="about-us_view"),
    path('contact-us', views.ContactUsView.as_view(), name="contact-us_view"),
    path('home', views.HomePageView.as_view(), name="home_view"),
    path('registration', views.UserRegistrationView.as_view(), name="registration_view"),
    path('job-offers', views.JobOffersView.as_view(), name="job-offers_view"),
    path('settings', views.SettingsView.as_view(), name="settings_view"),
    path('logout', views.LogOutView.as_view(), name="logout_view"),
    path('mailsent', views.MailSentView.as_view(), name="mailsent_view"),
    path('job-interview', views.JobInterviewView.as_view(), name="job-interview_view"),
    path('job-interview/question-1', views.JobInterviewQ1View.as_view(), name="job-interview_q1"),
    path('job-interview/question-2', views.JobInterviewQ2View.as_view(), name="job-interview_q2"),
    path('job-interview/question-3', views.JobInterviewQ3View.as_view(), name="job-interview_q3"),
    path('job-interview/question-4', views.JobInterviewQ4View.as_view(), name="job-interview_q4"),
    path('job-interview/question-5', views.JobInterviewQ5View.as_view(), name="job-interview_q5"),
    path('job-interview/question-6', views.JobInterviewQ6View.as_view(), name="job-interview_q6"),
    path('job-interview/question-7', views.JobInterviewQ7View.as_view(), name="job-interview_q7"),
    path('job-interview/question-8', views.JobInterviewQ8View.as_view(), name="job-interview_q8"),
    path('job-interview/question-9', views.JobInterviewQ9View.as_view(), name="job-interview_q9"),
    path('job-interview/question-10', views.JobInterviewQ10View.as_view(), name="job-interview_q10"),
]