from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address = models.TextField()
    contact_no = models.CharField(max_length=10)