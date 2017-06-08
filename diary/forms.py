from django import forms
from .models import Diary,Media

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'date','content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'標題（必填）', 'class':'form-control m-1'}),
            'date': forms.DateInput(attrs={'placeholder':'2017-06-01（必填）', 'id':'datepicker' , 'class': 'form-control m-1'}),
            'content': forms.Textarea(attrs={'class': 'form-control m-1'}),
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'img']
        widgets ={
            'title': forms.TextInput(attrs={'class':'form-control ', 'style':'width:200px ; display:inline'}),
            'description': forms.Textarea(attrs={'class': 'form-control ', 'style': 'width:300px ;height:100px;margin-left:20px'}),
            'img':forms.FileInput(attrs={'class':'btn btn-default'})
        }

