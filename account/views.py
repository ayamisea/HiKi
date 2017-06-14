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

def editAccount(request, pk) :
	if request.method =="POST":
		accID = request.session['accountID']
		acc = Account.objects.get(id=accID)
		account_form = AccountForm(request.POST)
		if account_form.is_valid() :
			acc.date = account_form.cleaned_data['date']
			acc.type = account_form.cleaned_data['type']
			acc.subtype = account_form.cleaned_data['subtype']
			acc.price = account_form.cleaned_data['price']
			acc.notes = account_form.cleaned_data['notes']
			acc.save()
	acc = Account.objects.get(id=pk)
	account_form = AccountForm(initial={
        'date': acc.date,
        'type':acc.type,
        'subtype':acc.subtype,
        'price':acc.price,
        'notes':acc.notes})
	request.session['accountID'] = pk
	return render(request, 'account/edit.html', locals())





