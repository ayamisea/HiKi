from django import forms
from .models import Diary,Media

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'date','type','content']
        date = forms.DateField(input_formats = ['%Y-%m-%d'])
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'標題（必填）', 'class':'form-control m-1'}),
            'date': forms.DateInput(attrs={'placeholder':'2017-06-01（必填）', 'id':'datepicker' , 'class': 'form-control m-1'}),
            'content': forms.Textarea(attrs={'class': 'form-control m-1'}),
            'type':forms.Select(attrs={'class':'form-control'})
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'img']
        widgets ={
            'title': forms.TextInput(attrs={'placeholder':'給圖片取個名字嘛？', 'class':'form-control', 'style':'display:inline;width:100%;'}),
            'description': forms.Textarea(attrs={'placeholder':'說一說這張圖片吧？', 'rows':'2','class': 'form-control', 'style':'width:100%;display:inline-block;'}),
            'img':forms.FileInput(attrs={'class':'custom-file-input', 'style':'width:100%;display:inline-block;'})
        }

