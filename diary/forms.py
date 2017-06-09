from django import forms
from .models import Diary,Media

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'date','content']
        date = forms.DateField(input_formats = ['%Y-%m-%d'])
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
            'title': forms.TextInput(attrs={'placeholder':'給圖片取個名字嘛？', 'class':'form-control ', 'style':'display:inline;width:100%;'}),
            'description': forms.Textarea(attrs={'placeholder':'說一說這張圖片吧？', 'class': 'form-control ', 'style':'width:100%;'}),
            'img':forms.FileInput(attrs={'class':'btn btn-default', 'style':'width:100%;'})
        }

