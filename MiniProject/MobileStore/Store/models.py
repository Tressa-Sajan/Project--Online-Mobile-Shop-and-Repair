
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(primary_key=True, unique=True)
    username = models.CharField(max_length=100, unique=True)
    userRole = models.CharField(max_length=10, default="customer") # customer, seller, admin

    def __str__(self):
        return self.username