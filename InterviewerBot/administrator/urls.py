from django.urls import path
from . import views

#path arranged alphabetically by name
app_name= 'administrator'
urlpatterns=[
    #path('api/data', views.get_data, name='api-data'),

    #TEST URL
    path('create-job', views.CreateJobView.as_view(), name="create-job_view"),
    path('dashboard', views.DashboardView.as_view(), name="dashboard_view"),
    path('job-lists', views.JobListsView.as_view(), name="job-lists_view"),
]