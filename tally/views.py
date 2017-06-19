from django.shortcuts import render, redirect
from .models import Tally
from .forms import TallyForm, DateForm
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


# Create your views here.

#display all
@login_required
def display(request) :
	user = request.user
	tallyList = request.user.tally_set.all()
	return render(request, 'tally/display.html', locals())

#display detail
@login_required
def detail(request, pk) :
	user = request.user
	tally = Tally.objects.get(pk=pk)
	if request.method == 'POST' :
		if 'delete' in request.POST :
			t = Tally.objects.get(pk=pk)
			t.delete()
			return HttpResponseRedirect('/tally/')
	return render(request, 'tally/detail.html', locals())

#create account

@login_required
def newTally(request) :
	user = request.user
	tally_form = TallyForm()
	if request.method == 'POST' :
		tally_form = TallyForm(request.POST)
		if tally_form.is_valid() :
			new_tally = tally_form.save(commit=True)
			new_tally.userID =  request.user
			new_tally.save()
			return HttpResponseRedirect('/tally/')
	return render(request, 'tally/newTally.html', locals())

@login_required
def editTally(request, pk) :
	user = request.user
	if request.method == "POST" :
		tallyID = request.session['tallyID']
		tally = Tally.objects.get(id=tallyID)
		tally_form = TallyForm(request.POST)
		if tally_form.is_valid() :
			tally.date = tally_form.cleaned_data['date']
			tally.type = tally_form.cleaned_data['type']
			tally.subtype = tally_form.cleaned_data['subtype']
			tally.price = tally_form.cleaned_data['price']
			tally.notes = tally_form.cleaned_data['notes']
			tally.save()
		return HttpResponseRedirect('/tally/')
	tally = Tally.objects.get(id=pk)
	tally_form = TallyForm(initial={
        'date': tally.date,
        'type':tally.type,
        'subtype':tally.subtype,
        'price':tally.price,
        'notes':tally.notes})
	request.session['tallyID'] = pk
	return render(request, 'tally/edit.html', locals())

@login_required
def summary(request) :
	user = request.user
	date_form = DateForm()
	tallyList = []
	if request.method == 'POST' :
		date_form = DateForm(request.POST)
		if date_form.is_valid() :
			tallyList = Tally.objects.filter(userID = request.user,date__range=[date_form.cleaned_data['dateA'], date_form.cleaned_data['dateB']])
		else :
			tallyList = request.user.tally_set.all()
	else :
		tallyList = request.user.tally_set.all()
	price_income_List = []
	price_expend_List = []
	total_income = 0
	total_expend = 0
	for tally in tallyList :
		d = False
		isIncome = False
		for str in Tally.PAY_CHOICES[0][1] :
			if str[0] == tally.type :
				isIncome = True
				break
		if isIncome :
			total_income = total_income + tally.price
			for pl in price_income_List :
				if pl[0] == tally.type :
					pl[1] = pl[1] + tally.price
					d = True
					break
			if d == False :
				tmpList = []
				tmpList.append(tally.type)
				tmpList.append(tally.price)
				price_income_List.append(tmpList)
		else :
			total_expend = total_expend + tally.price
			for pl in price_expend_List :
				if pl[0] == tally.type :
					pl[1] = pl[1] + tally.price
					d = True
					break
			if d == False :
				tmpList = []
				tmpList.append(tally.type)
				tmpList.append(tally.price)
				price_expend_List.append(tmpList)
	return render(request, 'tally/summary.html', locals())

@login_required
def delete(request, pk):
    if request.user.is_valid_user:
        tally = Tally.objects.get(pk=pk)
        tally.delete()
        return redirect('user_dashboard')
    return redirect(settings.LOGIN_URL)
