from django.db import models
from django.utils import timezone
from decimal import Decimal
from djchoices import DjangoChoices, ChoiceItem

from django.contrib.auth import get_user_model
User =  get_user_model()

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
	PAY_CHOICES = (
		('收入', (
			('打工', '打工'),
			('零用錢', '零用錢'),
			('其他收入', '其他收入'),
		) ), 
		('支出', (
			('食物', '食物'), 
			('玩樂' , '玩樂'),
			('交通', '交通'),
			('其他支出', '其他支出'),
		) ),
	)

	class MoneyTypes(DjangoChoices) :
		income = ChoiceItem()
	userID = models.ForeignKey(User,blank=True,null=True)
	date   = models.DateField(default=timezone.now)
	type   = models.CharField(max_length = 20, choices=PAY_CHOICES)
	subtype = models.CharField(max_length = 20)
	price  = models.DecimalField(max_digits=10,decimal_places=0,default=Decimal('0'))
	notes  = models.CharField(max_length=200)
	def __str__(self):
		return str(self.id)
	class Meta:
		ordering = ['date']

    