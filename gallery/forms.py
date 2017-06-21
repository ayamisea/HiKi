from django import forms

from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'img']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': '給圖片取個名字嘛？',
                    'class': 'form-control',
                    'style': 'display:inline;width:100%;',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'id': 'textarea',
                    'placeholder': '說一說這張圖片吧？',
                    'rows': '1',
                    'class': 'form-control',
                    'style': 'width:100%;display:inline-block;resize:none;overflow:hidden;',
                }
            ),
            'img': forms.FileInput(
                attrs={
                    'class': 'custom-file-input',
                    'style': 'width:100%;display:inline-block;',
                }
            ),
        }
