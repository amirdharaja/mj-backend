from __future__ import unicode_literals
from django.db import models

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import random
import os
import requests

ROLE = (
        ('', u''),
        ('U', u'User'),
        ('A', u'Admin'),
        ('SA', u'Admin'),
        ('DB', u'Delivery Boy'),
    )

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_active=True, is_admin=False, is_staff=False, first_name=None, last_name=None, email=None):
        if not phone:
            raise ValueError('Phone number required')
        if not password:
            raise ValueError('Password required')

        user_obj = self.model(phone=phone)

        user_obj.set_password(password)
        user_obj.staff= is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.email = email
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

class User(AbstractBaseUser):
    # phone_regax = RegexValidator(regex=r'^[3-9]\d{12}$', message='Enter valid phone number')
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    role = models.CharField(choices=ROLE, max_length=2, null=False, default='U')
    email = models.EmailField(null=True, unique=True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return self.phone

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active

    class Meta:
        db_table = "users"

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def crete_auth_token(sender, instanse=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instanse)