from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.filter(name='get_type')
def get_type(value,choices):
	if value in [ k for k,v in dict(choices)[_('Income')]]:
  		return 'income'
	if value in [ k for k,v in dict(choices)[_('Expense')]]:
  		return 'expense'

@register.filter(name='datelist')
def datelist(value):
	dates = sorted(set([ t.date for t in value ]),reverse=True)
	return(dates)

@register.filter(name='get_tally')
def get_tally(value,date):
	return( value.filter(date=date) )
