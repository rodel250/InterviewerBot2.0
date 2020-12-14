from django.db import models
from administrator.models import CreateJob


# Create your models here.

class Applicant(models.Model):
	firstname = models.CharField(max_length = 50, null=True, blank=True)
	lastname = models.CharField(max_length = 50, null=True, blank=True)
	phone = models.CharField(max_length = 11)
	password = models.CharField(max_length = 50, null=True, blank=True)
	gender = models.CharField(max_length = 10, null=True, blank=True)
	emailAddress = models.CharField(max_length = 50, null=True, blank=True)

	class Meta:
		db_table = "Applicant"

class Login(models.Model):
	user_id = models.IntegerField()
	emailAddress = models.CharField(max_length = 50, null=True, blank=True)
	password = models.CharField(max_length = 50, null=True, blank=True)

	class Meta:
		db_table = "currentUser"

class Contact(models.Model):
	email = models.EmailField(max_length=50)
	subject = models.CharField(max_length = 50)
	message = models.CharField(max_length = 500)

	class Meta:
		db_table = "Contact"
		
class SavedJobs(models.Model):
	user = models.ForeignKey(Applicant, null=False, blank=False, on_delete=models.CASCADE)
	job = models.ForeignKey(CreateJob, null=False, blank=False, on_delete=models.CASCADE)

	class Meta:
		db_table ="SavedJobs"

class AppliedJob(models.Model):
	user = models.ForeignKey(Applicant, null = False, blank = False, on_delete = models.CASCADE, related_name = "Applicant")
	job = models.ForeignKey(CreateJob, null = False, blank = False, on_delete = models.CASCADE, related_name = "CreateJob")
	response_1 = models.CharField(max_length = 250, null=True, blank=True)
	response_2 = models.CharField(max_length = 250, null=True, blank=True)
	response_3 = models.CharField(max_length = 250, null=True, blank=True)
	response_4 = models.CharField(max_length = 250, null=True, blank=True)
	response_5 = models.CharField(max_length = 250, null=True, blank=True)
	response_6 = models.CharField(max_length = 250, null=True, blank=True)
	response_7 = models.CharField(max_length = 250, null=True, blank=True)
	response_8 = models.CharField(max_length = 250, null=True, blank=True)
	response_9 = models.CharField(max_length = 250, null=True, blank=True)
	response_10 = models.CharField(max_length = 250, null=True, blank=True)
	response_11 = models.CharField(max_length = 250, null=True, blank=True)
	response_12 = models.CharField(max_length = 250, null=True, blank=True)
	response_13 = models.CharField(max_length = 250, null=True, blank=True)
	response_14 = models.CharField(max_length = 250, null=True, blank=True)
	response_15 = models.CharField(max_length = 250, null=True, blank=True)
	response_16 = models.CharField(max_length = 250, null=True, blank=True)
	response_17 = models.CharField(max_length = 250, null=True, blank=True)
	response_18 = models.CharField(max_length = 250, null=True, blank=True)
	response_19 = models.CharField(max_length = 250, null=True, blank=True)
	response_20 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_1 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_2 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_3 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_4 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_5 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_6 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_7 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_8 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_9 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_10 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_11 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_12 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_13 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_14 = models.CharField(max_length = 250, null=True, blank=True)
	requirement_15 = models.CharField(max_length = 250, null=True, blank=True)

	class Meta:
		db_table = "AppliedJob"
