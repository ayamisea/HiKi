from django import forms
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    pass

class UserChangeForm(forms.ModelForm):
    pass
