from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        WORKER="SELLER",'Seller'
        MEMBER="PRODUCT",'Product'
        USER="USER",'User'


    role = models.CharField(max_length=50,choices=Role.choices)