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

    question_1 = models.CharField(max_length = 250, null=True, blank=True, default='Please tell me about yourself.', editable=False)
    question_2 = models.CharField(max_length = 250, null=True, blank=True, default='What do you consider as your weakness?', editable=False)
    question_3 = models.CharField(max_length = 250, null=True, blank=True, default='What are your goals?', editable=False)
    question_4 = models.CharField(max_length = 250, null=True, blank=True, default='What are your actions if employees disagreed with your decision?', editable=False)
    question_5 = models.CharField(max_length = 250, null=True, blank=True, default='What can you do for us that other candidates cannot?', editable=False)
    question_6 = models.CharField(max_length = 250, null=True, blank=True, default='Describe a situation where results went against expectations. How did you adapt to this change?', editable=False)
    question_7 = models.CharField(max_length = 250, null=True, blank=True, default='Can you discuss a time where you had to manage your team through a difficult situation?', editable=False)
    question_8 = models.CharField(max_length = 250, null=True, blank=True, default='How do you prioritize your tasks when you have multiple deadlines to meet?', editable=False)
    question_9 = models.CharField(max_length = 250, null=True, blank=True, default='What is the most significant problem you solved in the workplace?', editable=False)
    question_10 = models.CharField(max_length = 250, null=True, blank=True, default='How do you explain new topics to coworkers unfamiliar with them?', editable=False)
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

    class Meta: 
        db_table = "CreateJob"


class currentJob(models.Model):
    jobID = models.IntegerField()
    
    class Meta:
        db_table = "currentJob"

class currentApplicant(models.Model):
    applicantID = models.IntegerField()
    
    class Meta:
        db_table = "currentApplicant"