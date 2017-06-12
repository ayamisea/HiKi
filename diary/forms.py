from django import forms
from .models import Diary,Media

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'date','type','content']
        date = forms.DateField(input_formats = ['%Y-%m-%d'])
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'標題（必填）', 'class':'form-control m-1'}),
            'date': forms.DateInput(attrs={'id':'datepicker' , 'placeholder':'2017-06-01（必填）', 'class': 'form-control m-1'}),
            'content': forms.Textarea(attrs={'id':'textarea','class': 'form-control m-1', 'style':'overflow: hidden;'}),
            'type':forms.Select(attrs={'class':'form-control m-1'})
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'img']
        widgets ={
            'title': forms.TextInput(attrs={'placeholder':'給圖片取個名字嘛？', 'class':'form-control', 'style':'display:inline;width:100%;'}),
            'description': forms.Textarea(attrs={'id':'textarea','placeholder':'說一說這張圖片吧？', 'rows':'1','class': 'form-control', 'style':'width:100%;display:inline-block;resize:none;overflow:hidden;'}),
            'img':forms.FileInput(attrs={'class':'custom-file-input', 'style':'width:100%;display:inline-block;'})
        }

