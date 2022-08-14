from django.db import models

# Create your models here.
class chequeInfo(models.Model):
    party_name = models.CharField(max_length=80,null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    cheque_number = models.CharField(max_length=15, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    account_holders_name = models.CharField(max_length=50, null=True, blank=True)
    cheque_received_date = models.DateField()
    cheque_due_date = models.DateField()
    partial_payment_received = models.FloatField(default=0.0)
    cheque_released = models.BooleanField(default=False)
    cheque_released_date = models.DateField(null=True, blank=True)
    notes_about_transaction = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.party_name


   