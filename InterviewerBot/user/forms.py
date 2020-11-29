from django import forms
from .models import *

class ApplicantForm(forms.ModelForm):
	
	class Meta:
		model = Applicant
		fields = ('firstname','lastname','password', 'gender', 'emailAddress')

class LoginForm(forms.ModelForm):

	class Meta:
		model = Login
		fields = ('emailAddress', 'password')

class UpdateForm(forms.ModelForm):

	class Meta:
		model = Applicant
		fields = ('firstname', 'lastname', 'password', 'emailAddress')