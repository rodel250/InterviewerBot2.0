from django import forms
from .models import *

class AdministratorForm(forms.ModelForm):

	class Meta:
		model = Administrator
		fields = ('firstname','lastname','password', 'gender', 'emailAddress')

class UpdateForm(forms.ModelForm):

	class Meta:
		model = Administrator
		fields = ('firstname', 'lastname', 'password', 'emailAddress')