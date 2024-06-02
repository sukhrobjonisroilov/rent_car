from django.db import models

from core.models.auth import User
from datetime import datetime as dt


class Brand(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    ctg = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    raqam = models.CharField(verbose_name="Davlat raqami", max_length=15)
    xk = models.TextField(null=True, blank=True)  # xarakteristika
    price = models.IntegerField(default=0, verbose_name="Kunlik ijara narxi")
    status = models.BooleanField(verbose_name="Ijaraga mumkinmi?", default=True)  # activ, aktiv emasligi
    yili = models.IntegerField(verbose_name="Ishlab chiqarilgan yil", default=2015)
    img = models.ImageField(upload_to='cars')


class Arenda(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField(default=dt.today().strftime(f"%Y-%m-0{dt.today().day + 1}"))
    summa = models.BigIntegerField(default=0)
    status = models.SmallIntegerField(default=0, choices=[

        (0, "tasdiqlanmagan"),
        (1, "tasdiqlangan"),
        (2, "tugatilgan"),
        (3, "Bekor qilingan"),
    ])
    pay_type = models.CharField(max_length=25, choices=[
        ("Naqt", "Naqt"),
        ("Plastik", "Plastik"),
        ("Bo'lib to'lash", "Bo'lib to'lash"),
    ])

    def get_status(self):
        return {
            0: "Tasdiqlanmagan",
            1: "Tasdiqlangan",
            2: "Tugagan",
            3: "Bekor qilingan"
        }[self.status]
