from django.shortcuts import render
from .models import Account
from .forms import AccountForm
from django.http import HttpResponseRedirect

# Create your views here.

#display all
def display(request) :
	accountList = Account.objects.all()
	return render(request, 'account/display.html', locals())

#display detail
def detail(request, pk) :
	account = Account.objects.get(pk=pk)
	if request.method == 'POST' :
		if 'delete' in request.POST :
			a = Account.objects.get(pk=pk)
			a.delete()
			return HttpResponseRedirect('/account/')
	return render(request, 'account/detail.html', locals())

#create account
def newAccount(request) :
	account_form = AccountForm()
	if request.method == 'POST' :
		account_form = AccountForm(request.POST)
		if account_form.is_valid() :
			new_account = account_form.save(commit=True) 
			new_account.save()
	return render(request, 'account/newAccount.html', locals())
