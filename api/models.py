import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


# Create your models here.
class Wallet(models.Model):

    def deposit(self, amount):
        if self.is_valid(amount):
            self.balance += amount
            self.save()

    def withdraw(self, amount):
        if self.is_valid(amount):
            if self.balance >= amount:
                self.balance -= amount
                self.save()
            else:
                raise ValueError("Not enough balance")

    @staticmethod
    def is_valid(amount):
        if amount <= 0:
            raise ValueError("Amount must be bigger than zero")
        return True


    class Currency(models.TextChoices):
        RUB = 'RUB', 'Ruble'
        USD = 'USD', 'Dollar'
        EURO = 'EUR', 'Euro'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def get_absolute_url(self):
        return reverse('wallet_details', args=[self.uuid])
