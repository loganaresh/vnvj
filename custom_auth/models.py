from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile_number = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    
