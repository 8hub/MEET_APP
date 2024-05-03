from django.contrib.auth.models import AbstractUser, BaseUserManager
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
            raise ValidationError("Invalid email address")
        
        try:
            validate_password(password, user=user)
            user.set_password(password)
        except ValidationError as e:
            raise ValidationError(e)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not all([extra_fields.get("is_staff"), extra_fields.get("is_superuser")]):
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    # override the default Manager
    objects = CustomUserManager()