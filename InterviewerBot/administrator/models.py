from django.db import models

# Create your models here.

class Administrator(models.Model):
	firstname = models.CharField(max_length = 50, null=True, blank=True)
	lastname = models.CharField(max_length = 50, null=True, blank=True)
	phone = models.CharField(max_length = 11)
	password = models.CharField(max_length = 50, null=True, blank=True)
	gender = models.CharField(max_length = 10, null=True, blank=True)
	emailAddress = models.CharField(max_length = 50, null=True, blank=True)

	class Meta:
		db_table = "Administrator"

class Joblist(models.Model):
	job_header = models.CharField(max_length = 50, null=False)
	job_description = models.CharField(max_length = 250, null=False)

	class Meta:
		db_table ="Joblist"