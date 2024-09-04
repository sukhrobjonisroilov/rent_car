from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class UserMG(UserManager):
    def create_user(self, username, password=None, is_staff=False, is_superuser=False,
                    **extra_fields):
        user = self.model(
            username=username,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    # admin

    username = models.CharField(max_length=20, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.SmallIntegerField(choices=[
        (1, "Admin"),
        (2, "User"),
    ], default=1)

    objects = UserMG()

    REQUIRED_FIELDS = [ 'user_type']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
