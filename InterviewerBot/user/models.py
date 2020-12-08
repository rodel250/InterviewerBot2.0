from django.db import models

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
	job_id = models.IntegerField()
	job_header = models.CharField(max_length = 50, null=False)
	job_description = models.CharField(max_length = 250, null=False)

	class Meta:
		db_table ="SavedJobs"