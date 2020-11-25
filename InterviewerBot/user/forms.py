from django import forms
from .models import *

class ApplicantForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta:
		model = Applicant
		fields = ('firstname','lastname','password', 'gender', 'emailAddress')