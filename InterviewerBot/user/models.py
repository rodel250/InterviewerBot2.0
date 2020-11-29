from django.db import models
from datetime import datetime

# Create your models here.

class Applicant(models.Model):
	firstname = models.CharField(max_length = 50)
	lastname = models.CharField(max_length = 50)
	password = models.CharField(max_length = 50)
	gender = models.CharField(max_length = 10)
	emailAddress = models.CharField(max_length = 50)

	class Meta:
		db_table = "Applicant"

# class JobOffer(models.Model):
# 	jobName = models.CharField(max_length = 20)
# 	jobDescription = models.TextField()
# 	jobRequirements = models.TextField()
# 	jobPicture = models.FileField()

# 	class Meta: 
# 		db_table = "Job"

# class Administrator(models.Model):
# 	firstName = models.CharField(max_length = 50)
# 	middleName = models.CharField(max_length = 50)
# 	lastName = models.CharField(max_length = 50)
# 	birthDate = models.DateField()
# 	age = models.IntegerField()
# 	gender = models.CharField(max_length = 10)
# 	emailAddress = models.CharField(max_length = 10)