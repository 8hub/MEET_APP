from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if email is not None:
            # validate the email before it is stored in the database
            # if the email is not valid raise ValidationError
            validate_email(email)
        else:
            raise ValueError("Users must have an email")
        if password is not None:
            # validate the password before it is hashed
            # if the password is not valid raise ValidationError
            validate_password(password, user=self.model(username=username, email=email, **extra_fields))
        else:
            raise ValueError("The password must be set")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        # hash the password to store it in the database
        user.set_password(password) 
        user.save(using=self._db)
        return user


class User(AbstractUser):
    # override the default Manager
    objects = CustomUserManager()