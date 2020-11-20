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
    path('job-interview', views.JobInterviewView.as_view(), name="job-interview_view"),
    path('registration', views.UserRegistrationView.as_view(), name="registration_view"),
    path('job-offers', views.JobOffersView.as_view(), name="job-offers_view"),
]