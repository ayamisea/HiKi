from django import forms
from .models import Diary,Media

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'date','content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control ' , 'style':'width:200px ; display:inline'}),
            'date': forms.DateInput(attrs={'id':'datepicker' , 'class': 'form-control ' , 'style':'width:200px ; display:inline'}),
            'content': forms.Textarea(attrs={'class': 'form-control ', 'style': 'width:300px ;margin-left:20px'}),
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'img']

