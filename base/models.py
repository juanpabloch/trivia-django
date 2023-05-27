from django.db import models
from accounts.models import CustomUser
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# class Player(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     country = models.CharField(max_length=255, null=True, blank=True)
#     points = models.IntegerField(default=1000)
#     q_answered = models.IntegerField(default=0)
#     q_correctly = models.IntegerField(default=0)
#     q_history = models.TextField(default='{}')
#     active = models.SmallIntegerField(default=1)
#     banned = models.SmallIntegerField(default=0)
#     register = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#     last_login = models.DateTimeField(null=True)
    
#     def __str__(self):
#         return self.user.email
    
#     def add_points(self, points):
#         self.points += points
#         self.save()
    
#     def subtract_points(self, points):
#         self.points -= points
#         self.save()
        
#     def add_answered(self):
#         self.q_answered += 1
#         self.save() 
    
#     def add_correctly(self):
#         self.q_correctly += 1
#         self.save() 
        
#     def set_bet(self, percentage):
#         bet = int(percentage) * self.points / 100
#         return bet
      
#     class Meta:
#         db_table = 'player'
#         verbose_name_plural = 'Players'    
  

class Category(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        