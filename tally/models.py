from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem

User =  get_user_model()

class Tally(models.Model) :
    PAY_CHOICES = (
        (_('Income'), (
            (_('Part-time Job'), _('Part-time Job')),
            (_('Pocket Money'), _('Pocket Money')),
            (_('Other incomes'), _('Other incomes')),
        )),
        (_('Expense'), (
            (_('Food'), _('Food')),
            (_('Entertainment'), _('Entertainment')),
            (_('Traffic'), _('Traffic')),
            (_('Other expenses'), _('Other expenses')),
        )),
    )

    user = models.ForeignKey(User, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    pay_type = models.CharField(max_length=20, choices=PAY_CHOICES, default=PAY_CHOICES[1][1][0][0])
    subtype = models.CharField(max_length=20, blank=True)
    cash = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('0'))
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
    	if self.subtype:
    		return '{} {}->{} ${}'.format(self.date, self.pay_type, self.subtype , self.cash)
    	else:
        	return '{} {} ${}'.format(self.date, self.pay_type, self.cash)

    class MoneyTypes(DjangoChoices) :
        income = ChoiceItem()

    class Meta:
        ordering = ['date']
