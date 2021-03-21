import uuid

from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        if not first_name:
            raise ValueError('User must have first name')
        if not last_name:
            raise ValueError('User must have last name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):

        user = self.create_user(
            email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30)
    userId = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name='first_name', max_length=100)
    last_name = models.CharField(verbose_name='last_name', max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=256, blank=True, null=True)
    isAuthor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_admin
