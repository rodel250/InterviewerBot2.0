from django.urls import path
from . import views

#path arranged alphabetically by name
app_name= 'administrator'
urlpatterns=[
    #path('api/data', views.get_data, name='api-data'),

    #TEST URL
    path('dashboard', views.DashboardView.as_view(), name="dashboard_view"),
    path('job-lists', views.JobListsView.as_view(), name="job-lists_view"),
    path('add-admin', views.AdminRegistrationView.as_view(), name="add-admin_view"),
    path('settings', views.SettingsView.as_view(), name="settings_view"),
    path('applicants',views.Applicants.as_view(), name="applicants_view"),
    path('applicant/response', views.ResponseView.as_view(), name="response_view"),
    path('logout', views.LogOutView.as_view(), name="logout_view")
]