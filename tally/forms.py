from django import forms

from .models import Tally

class TallyForm(forms.ModelForm):
    class Meta:
        model = Tally
        pay_type = forms.ChoiceField(
            choices=Tally.PAY_CHOICES,
            widget=forms.Select(attrs={'class':'hidden'}),
        )
        fields = ['date', 'pay_type', 'subtype', 'cash', 'notes']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'id':'datepicker',
                    'class': 'form-control m-1 w-100',
                    'style':'display:inline',
                }
            ),
            'subtype': forms.TextInput(
                attrs={
                    'class':'form-control m-1 w-100',
                    'style':'display:inline',
                }
            ),
            'cash':forms.TextInput(
                attrs={
                    'class':'form-control m-1 w-100',
                    'style':'display:inline',
                }
            ),
            'notes':forms.Textarea(
                attrs={
                    'id':'textarea',
                    'class':'form-control m-1 w-100',
                    'style':'display:inline',
                }
            ),
        }

class DateForm(forms.Form):
    dateA = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'datepicker form-control',
                'style':'width:45%;min-width:120px;',
            }
        ),)
    dateB = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'datepicker form-control',
                'style':'width:45%;min-width:120px;',
            }
        ),)
