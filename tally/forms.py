from django import forms
from .models import Tally
from django.db import models
from django.utils import timezone

class TallyForm(forms.ModelForm) :
	class Meta :
		model  = Tally
		fields = ['date', 'pay_type', 'type', 'subtype', 'price', 'notes']
		widgets = {
            'date': forms.DateInput(attrs={'id':'datepicker' , 'class': 'form-control ' , 'style':'width:200px ; display:inline'}),
            'pay_type': forms.Select(attrs={'class':'form-control m-1'}),
            'type': forms.Select(attrs={'class':'form-control m-1'}),
            'subtype': forms.TextInput(attrs={'class':'form-control', 'style':'width:200px ; display:inline'}),
        }

class DateForm(forms.Form) :
	dateA = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
	dateB = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
