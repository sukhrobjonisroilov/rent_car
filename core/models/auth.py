from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class UserMG(UserManager):
    def create_user(self, seria_ps, phone=None, password=None, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(
            seria_ps=seria_ps,
            phone=phone,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, seria_ps, phone=None, password=None, **extra_fields):
        return self.create_user(
            seria_ps=seria_ps,
            phone=phone,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    # admin
    fio = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)
    seria_ps = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)

    # Prava
    g_year = models.DateField(verbose_name="Guvohnoma Yili", null=True, blank=True)
    g_seria = models.CharField(verbose_name="Guvohnoma Seriasi", max_length=20, null=True, blank=True)
    g_ctg = models.CharField(verbose_name="Guvohnoma Toifasi", max_length=3, null=True, blank=True)

    # obshiy
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.SmallIntegerField(choices=[
        (1, "Admin"),
        (2, "User"),
    ], default=2)

    objects = UserMG()

    REQUIRED_FIELDS = ['phone', 'user_type']
    USERNAME_FIELD = 'seria_ps'

    def get_user_name(self):
        return f"{self.fio.split()[0] if not self.username else self.username} "
