from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email address")
        
        try:
            validate_password(password, user=user)
            user.set_password(password)
        except ValidationError as e:
            raise ValueError(e)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    # override the default Manager
    objects = CustomUserManager()