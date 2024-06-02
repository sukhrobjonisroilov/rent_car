from django.db import models

from base.helper import card_mask
from core.models.auth import User


class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default="Rent Card")
    number = models.CharField(max_length=20)  # 8524 9666 6666 6666
    mask = models.CharField(max_length=20, null=True, blank=True)  # 8524 **** **** 6666
    expire = models.CharField(max_length=5)  # 25/12
    token = models.CharField(max_length=256, unique=True)
    balance = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.mask

    def save(self, *args, **kwargs):
        self.mask = card_mask(self.number)
        return super(Card, self).save(*args, **kwargs)


class Monitoring(models.Model):
    tr_id = models.CharField(max_length=128, unique=True)
    sender = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name='sender')
    receiver = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name='receiver')
    amount = models.IntegerField(default=0)
    status = models.SmallIntegerField(default=1)  # 1-created, 2 -o'tqazildi, 3 atmen
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.tr_id






