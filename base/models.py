from django.db import models
from accounts.models import CustomUser
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager    
  

class Category(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        