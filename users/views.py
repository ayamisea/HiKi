from django.contrib.auth import login
from django.shortcuts import redirect, render, HttpResponse
from django.utils.translation import ugettext

from .forms import UserCreationForm


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return HttpResponse('Successed!')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
