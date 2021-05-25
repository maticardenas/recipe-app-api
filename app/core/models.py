from typing import Optional, TYPE_CHECKING

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> "User":
        """Creates and saves a new User"""
        if not email:
            raise ValueError

        user = self.model(email=self.normalize_email(email), **extra_fields)
        # To store the password encrypted
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: Optional[str] = None) -> "User":
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    """ Ingredient to be used in a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name