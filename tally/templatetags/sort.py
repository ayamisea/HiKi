from django import template

register = template.Library()

@register.filter(name='datelist')
def datelist(value):
	dates = sorted(set([ t.date for t in value ]),reverse=True)	
	return(dates)

@register.filter(name='get_tally')
def get_tally(value,date):
	return( value.filter(date=date) )