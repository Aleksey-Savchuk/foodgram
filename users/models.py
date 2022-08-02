from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


# User = get_user_model()
class User(AbstractUser):

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    password = models.CharField(
        max_length=128,
        blank=True,
        null=False,
    )
    email = models.EmailField('Email адрес', unique=True, null=False)
    username = models.CharField(max_length=150, unique=True)

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=100,
        null=False,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

