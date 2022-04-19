from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(username, password, **other_fields)

    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError(
                'You must provide username'
            )
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def find_by_email(self, email: str) -> object:
        return self.filter(email=email).first()

    def find_by_username(self, username: str) -> object:
        return self.filter(username=username).first()

    def register_user(self, payload: dict) -> object:
        user = self.model(username=payload.get('username'),
                          email=payload.get('contact_email'),
                          first_name=payload.get('first_name'),
                          last_name=payload.get('last_name'))
        user.set_password(payload.get('password'))
        user.save()
        return user

    def find_users_by_role(self, role: str) -> object:
        return self.filter(role__icontains=role)

    def register_admin(self, payload: dict) -> object:
        user = self.model(username=payload.get('username'),
                          email=payload.get('email'),
                          first_name=payload.get('first_name'),
                          last_name=payload.get('last_name'))
        user.set_password(payload.get('password'))
        user.save()
        return user


"""
    USER MODEL
"""


class Users(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    image = models.ImageField(null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    objects = CustomUserManager()

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username}'
