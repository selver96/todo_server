from .token import *

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, surname, name, email, username=None, password=None):
        user = self.model(surname=surname, name=name, username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, surname, name, email, username, password=None):
        user = self.create_user(surname=surname, name=name, username=username,
                                email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    surname = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def access(self):
        return access(self.pk, self.name, self.surname, self.email)

    @property
    def refresh(self):
        return refresh(self.pk, self.name, self.surname, self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class Token(models.Model):
    token = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.name


class TaskGroup(models.Model):
    title = models.CharField(max_length=150)
    for_completed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=150)
    is_completed = models.BooleanField(default=False)
    end_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title
