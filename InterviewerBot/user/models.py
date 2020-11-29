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
	emailAddress = models.CharField(max_length = 50, null=True, blank=True)
	password = models.CharField(max_length = 50, null=True, blank=True)

	class Meta:
		db_table = "currentUser"

class Contact(models.Model):
	email = models.EmailField(max_length=50)
	subject = models.CharField(max_length = 50)
	message = models.CharField(max_length = 100)

	class Meta:
		db_table = "Contact"
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