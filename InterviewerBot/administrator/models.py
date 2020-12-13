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

class CreateJob(models.Model):
    admin = models.ForeignKey(Administrator, null = False, blank = False, on_delete = models.CASCADE, related_name = "Administrator")
    title = models.CharField(max_length = 50, null=True, blank=True)
    description = models.CharField(max_length = 500, null=True, blank=True)

    question_1 = models.CharField(max_length = 250, null=True, blank=True)
    question_2 = models.CharField(max_length = 250, null=True, blank=True)
    question_3 = models.CharField(max_length = 250, null=True, blank=True)
    question_4 = models.CharField(max_length = 250, null=True, blank=True)
    question_5 = models.CharField(max_length = 250, null=True, blank=True)
    question_6 = models.CharField(max_length = 250, null=True, blank=True)
    question_7 = models.CharField(max_length = 250, null=True, blank=True)
    question_8 = models.CharField(max_length = 250, null=True, blank=True)
    question_9 = models.CharField(max_length = 250, null=True, blank=True)
    question_10 = models.CharField(max_length = 250, null=True, blank=True)
    question_11 = models.CharField(max_length = 250, null=True, blank=True)
    question_12 = models.CharField(max_length = 250, null=True, blank=True)
    question_13 = models.CharField(max_length = 250, null=True, blank=True)
    question_14 = models.CharField(max_length = 250, null=True, blank=True)
    question_15 = models.CharField(max_length = 250, null=True, blank=True)
    question_16 = models.CharField(max_length = 250, null=True, blank=True)
    question_17 = models.CharField(max_length = 250, null=True, blank=True)
    question_18 = models.CharField(max_length = 250, null=True, blank=True)
    question_19 = models.CharField(max_length = 250, null=True, blank=True)
    question_20 = models.CharField(max_length = 250, null=True, blank=True)

    requirement1 = models.CharField(max_length = 250, null=True, blank=True)
    requirement2 = models.CharField(max_length = 250, null=True, blank=True)
    requirement3 = models.CharField(max_length = 250, null=True, blank=True)
    requirement4 = models.CharField(max_length = 250, null=True, blank=True)
    requirement5 = models.CharField(max_length = 250, null=True, blank=True)
    requirement6 = models.CharField(max_length = 250, null=True, blank=True)
    requirement7 = models.CharField(max_length = 250, null=True, blank=True)
    requirement8 = models.CharField(max_length = 250, null=True, blank=True)
    requirement9 = models.CharField(max_length = 250, null=True, blank=True)
    requirement10 = models.CharField(max_length = 250, null=True, blank=True)
    requirement11 = models.CharField(max_length = 250, null=True, blank=True)
    requirement12 = models.CharField(max_length = 250, null=True, blank=True)
    requirement13 = models.CharField(max_length = 250, null=True, blank=True)
    requirement14 = models.CharField(max_length = 250, null=True, blank=True)
    requirement15 = models.CharField(max_length = 250, null=True, blank=True)

    class Meta: 
        db_table = "CreateJob"