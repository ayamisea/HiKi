from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext, ugettext_lazy as _

from users.decorators import user_valid

from .forms import DateForm, TallyForm
from .models import Tally

@login_required
@user_valid
def display(request):
    """Display all records.
    """
    tally_list = request.user.tally_set.all()
    choices = Tally.PAY_CHOICES

    return render(request, 'tally/display.html', locals())

@login_required
@user_valid
def detail(request, pk):
    """Display record details.
    """
    tally = get_object_or_404(request.user.tally_set, pk=pk)
    choices = Tally.PAY_CHOICES

    return render(request, 'tally/detail.html', locals())

@login_required
@user_valid
def new(request):
    """Create new record.
    """
    if request.method == 'POST':
        tally_form = TallyForm(request.POST)

        if tally_form.is_valid():
            new_tally = tally_form.save(commit=True)
            new_tally.user = request.user
            new_tally.save()

            messages.success(request, ugettext("Add a record successfully!"))

        return redirect('tally')
    else:
        tally_form = TallyForm()

    return render(request, 'tally/new.html', locals())

@login_required
@user_valid
def edit(request, pk):
    """Edit record.
    """
    tally = get_object_or_404(request.user.tally_set, pk=pk)

    if request.method == "POST":
        tally_form = TallyForm(request.POST, instance=tally)

        if tally_form.is_valid():
            tally_form.save()

            messages.success(request, ugettext("Complete editing this record!"))

        return redirect('tally')
    else:
        tally_form = TallyForm(instance=tally)

    return render(request, 'tally/edit.html', locals())

@login_required
@user_valid
def delete(request, pk):
    tally = get_object_or_404(request.user.tally_set, pk=pk)
    tally.delete()

    messages.success(request, ugettext("Successfully delete " + str(tally)))

    pre_url = request.GET.get('from', None)
    if pre_url:
        return redirect(pre_url)

    return redirect(settings.DASHBOARD_URL)

@login_required
@user_valid
def summary(request):
    #確認表單
    date_form = DateForm()

    if request.method == 'POST':
        date_form = DateForm(request.POST)

        if date_form.is_valid():
            date = date_form

            tally_list = request.user.tally_set.filter(
                user=request.user,
                date__range=[date_form.cleaned_data['dateA'], date_form.cleaned_data['dateB']])

    tally_list = request.user.tally_set.all()

    #製作圖表清單
    categories = {k: 0 for k, v in dict(Tally.PAY_CHOICES)[_('Income')]}
    length = len(categories)
    categories.update({k: 0 for k, v in dict(Tally.PAY_CHOICES)[_('Expense')]})

    for tally in tally_list:
        categories[_(tally.pay_type)] += int(tally.cash)

    income = list(categories.items())[:length]
    expense = list(categories.items())[length:]
    price_lists = [income, expense]
    total_prices = [sum([i[1] for i in income]), sum([i[1] for i in expense])]
    print(total_prices)
    return render(request, 'tally/summary.html', {
        'tallyList': tally_list,
        'price_lists': price_lists,
        'total_prices': total_prices,
        'date_form': date_form, })
