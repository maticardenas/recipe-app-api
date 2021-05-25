from typing import Optional, TYPE_CHECKING

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> "User":
        """Creates and saves a new User"""
        user = self.model(email=email, **extra_fields)
        # To store the password encrypted
        user.set_password(password)
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

