from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Diary

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'date', 'post_type', 'content']
        date = forms.DateField(input_formats=['%Y-%m-%d'])
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': _('標題（必填）'),
                    'class': 'form-control m-1',
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'id': 'datepicker',
                    'placeholder': _('2017-06-01（必填）'),
                    'class': 'form-control m-1',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'id': 'textarea',
                    'class': 'form-control m-1',
                    'style': 'overflow: hidden;',
                }
            ),
            'post_type':forms.Select(
                attrs={
                    'class': 'form-control m-1',
                }
            ),
        }
