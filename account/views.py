from django.shortcuts import render
from .models import Account

# Create your views here.

def display(request) :
	accountList = Account.objects.all()
	return render(request, 'account/display.html', locals())