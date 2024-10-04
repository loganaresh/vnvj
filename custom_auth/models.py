from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, mobile_number, first_name, last_name, email, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, mobile_number, first_name, last_name, email, password):
        user = self.create_user(
            username=username,
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_number', 'first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
