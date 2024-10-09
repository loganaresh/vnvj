from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, mobile_number, first_name, last_name, email, password=None):
        if not username:
            raise ValueError("The Username field is required")
        if not mobile_number:
            raise ValueError("The Mobile number field is required")
        if not email:
            raise ValueError("The Email field is required")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        if password:
            user.set_password(password)
        else:
            raise ValueError("The Password field is required")

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
    username = models.CharField(max_length=30, unique=True, verbose_name="Username")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email Address")
    mobile_number = models.CharField(max_length=15, unique=True, verbose_name="Mobile Number")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_staff = models.BooleanField(default=False, verbose_name="Staff Status")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date Joined")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_number', 'first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
