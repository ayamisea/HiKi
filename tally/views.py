from django.shortcuts import render
from .models import Tally
from .forms import TallyForm, DateForm
from django.http import HttpResponseRedirect
from django.db.models import Sum

# Create your views here.

#display all
def display(request) :
	tallyList = Tally.objects.all()
	return render(request, 'tally/display.html', locals())

#display detail
def detail(request, pk) :
	tally = Tally.objects.get(pk=pk)
	if request.method == 'POST' :
		if 'delete' in request.POST :
			t = Tally.objects.get(pk=pk)
			t.delete()
			return HttpResponseRedirect('/tally/')
	return render(request, 'tally/detail.html', locals())

#create account
def newTally(request) :
	tally_form = TallyForm()
	if request.method == 'POST' :
		tally_form = TallyForm(request.POST)
		if tally_form.is_valid() :
			new_tally = tally_form.save(commit=True) 
			new_tally.save()
			return HttpResponseRedirect('/tally/')
	return render(request, 'tally/newTally.html', locals())

def editTally(request, pk) :
	if request.method == "POST" :
		tallyID = request.session['tallyID']
		tally = Tally.objects.get(id=tallyID)
		tally_form = AccountForm(request.POST)
		if tally_form.is_valid() :
			tally.date = tally_form.cleaned_data['date']
			tally.type = tally_form.cleaned_data['type']
			tally.subtype = tally_form.cleaned_data['subtype']
			tally.price = tally_form.cleaned_data['price']
			tally.notes = tally_form.cleaned_data['notes']
			tally.save()
		return HttpResponseRedirect('/tally/')
	tally = Tally.objects.get(id=pk)
	tally_form = AccountForm(initial={
        'date': tally.date,
        'type':tally.type,
        'subtype':tally.subtype,
        'price':tally.price,
        'notes':tally.notes})
	request.session['tallyID'] = pk
	return render(request, 'tally/edit.html', locals())

def summary(request) :
	date_form = DateForm()
	tallyList = []
	if request.method == 'POST' :
		date_form = DateForm(request.POST)
		if date_form.is_valid() :
			tallyList = Tally.objects.filter(date__range=[date_form.cleaned_data['dateA'], date_form.cleaned_data['dateB']])
		else :
			tallyList = Tally.objects.all()
	else :
		tallyList = Tally.objects.all()
	priceList = []
	for tally in tallyList :
		d = False
		for pl in priceList :
			if pl[0] == tally.type :
				pl[1] = pl[1] + tally.price
				d = True
				break
		if d == False :
			tmpList = []
			tmpList.append(tally.type)
			tmpList.append(tally.price)
			priceList.append(tmpList)
	return render(request, 'tally/summary.html', locals())




