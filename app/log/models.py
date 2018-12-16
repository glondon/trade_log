from django.db import models
#from datetime import datetime
import datetime

# Create your models here.
#TODO update to match trade_log schema
class Logs(models.Model):
    positions = (
        ('long', 'long'),
        ('short', 'short')
    )
    statuses = (
        ('open', 'open'),
        ('closed', 'closed')
    )
    user_id = models.IntegerField()
    symbol = models.CharField(max_length=8)
    entry = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    exit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stop = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    target = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    position = models.CharField(max_length=5, choices=positions, default='long')
    entry_date = models.DateField(default=datetime.date.today)
    exit_date = models.DateField(default=None, blank=True, null=True)
    size = models.CharField(max_length=25)
    account = models.CharField(max_length=25) #TODO save user account names
    entry_comm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    exit_comm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    result = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    early_exit = models.BooleanField(default=False)
    trade_reasons = models.TextField(max_length=255)
    notes = models.TextField(max_length=500)
    status = models.CharField(max_length=6, choices=statuses, default='closed')
    exp_date = models.DateField(default=None, blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.datetime.now, blank=True) #TODO only need date

    def __str__(self):
        return self.symbol
    class Meta:
        verbose_name_plural = 'Logs'