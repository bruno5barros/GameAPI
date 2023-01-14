from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
import uuid
import os


def user_image_path(instance, filename):
    """Generate file name for new user image"""
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads/user/', filename)


class UserManager(BaseUserManager):

    def validate_fields(self, email, password=None, **extra_fields):
        """Validate user email field"""
        if not email:
            raise ValueError("An email must be provided")

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        self.validate_fields(email, password, **extra_fields)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and save a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    """Custom user model based on Django user to use email"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    birthdate = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_image_path, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "birthdate"]

    objects = UserManager()
