from django.contrib.auth.views import (
    login as base_login
)
from django.shortcuts import redirect, render, HttpResponse
from django.utils.translation import ugettext

from .forms import AuthenticationForm, PublicUserCreationForm


def user_signup(request):
    if request.method == 'POST':
        form = PublicUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            base_login(request, user)
            return HttpResponse('Successed!')
    else:
        form = PublicUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    return base_login(request, authentication_form=AuthenticationForm, template_name='users/login.html')
