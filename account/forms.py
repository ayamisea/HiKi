from django import forms
from .models import Account

class AccountForm(forms.ModelForm) :
	class Meta:
		model  = Account
		fields = ['date', 'type', 'subtype', 'price', 'notes']
		widgets = {
            'date': forms.DateInput(attrs={'id':'datepicker' , 'class': 'form-control ' , 'style':'width:200px ; display:inline'}),
            'type': forms.TextInput(attrs={'class':'form-control' , 'style':'width:200px ; display:inline'}),
            'subtype': forms.TextInput(attrs={'class':'form-control', 'style':'width:200px ; display:inline'}),
        }