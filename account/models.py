from django.db import models
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Account(models.Model) :
    date   = models.DateField(default=timezone.now)
    type   = models.CharField(max_length = 20)
    subtype = models.CharField(max_length = 20)
    price  = models.DecimalField(max_digits=10,decimal_places=0,default=Decimal('0'))
    notes  = models.CharField(max_length=200)
    