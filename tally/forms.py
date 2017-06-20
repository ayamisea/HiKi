from django import forms
from django.utils.translation import ugettext_lazy as _

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
            'cash': forms.TextInput(
                attrs={
                    'class':'form-control m-1 w-100',
                    'style':'display:inline',
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'id':'textarea',
                    'class':'form-control m-1 w-100',
                    'style':'display:inline',
                }
            ),
        }
        error_messages = {
            'cash': {
                'zero_negative': _('The cash field cannot be zero or negative')
            }
        }

    def clean(self):
        cleaned_data = super(TallyForm, self).clean()
        cash = cleaned_data.get('cash')
        if cash <= 0:
            self.add_error('cash', self.Meta.error_messages['cash']['zero_negative'])

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
