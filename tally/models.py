from django.db import models
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Tally(models.Model) :
	TYPE_CHOICES = ( 
		('食物', '食物'), 
		('玩樂' , '玩樂'),
		('交通', '交通'), 
		('其他', '其他'),
	)
	PAY_CHOICES = (
		('收入', '收入'),
		('支出', '支出'),
	)
	date   = models.DateField(default=timezone.now)
	pay_type = models.CharField(max_length = 20, choices = PAY_CHOICES, default = PAY_CHOICES[0][1])
	type   = models.CharField(max_length = 20, choices = TYPE_CHOICES, default = TYPE_CHOICES[3][1])
	subtype = models.CharField(max_length = 20)
	price  = models.DecimalField(max_digits=10,decimal_places=0,default=Decimal('0'))
	notes  = models.CharField(max_length=200)

    