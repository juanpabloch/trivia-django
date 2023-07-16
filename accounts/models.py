from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        
        if kwargs.get('is_staff') is not True:
            raise ValueError("Super user must have is_staff=True.")
        if kwargs.get('is_superuser') is not True:
            raise ValueError("Super user must have is_superuser=True.")

        return self.create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=160)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=255)
    # name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    points = models.IntegerField(default=1000)
    q_answered = models.IntegerField(default=0)
    q_correctly = models.IntegerField(default=0)
    q_history = models.TextField(default='{}')
    active = models.SmallIntegerField(default=1)
    banned = models.SmallIntegerField(default=0)
    register = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)
    request_points_key = models.CharField(max_length=255, null=True, blank=True)
    request_points_requested = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
        
    def __str__(self):
        return self.email
    
    def add_points(self, points):
        self.points += points
        self.save()
    
    def subtract_points(self, points):
        self.points -= points
        self.save()
        
    def add_answered(self):
        self.q_answered += 1
        self.save() 
    
    def add_correctly(self):
        self.q_correctly += 1
        self.save() 
    
    def get_player_stats(self):
        stats = {}
        stats["answer"] = self.q_answered
        stats["correctly"] = self.q_correctly
        stats["percentage"] = int((self.q_correctly * 100) / self.q_answered) if self.q_answered != 0 else 0
        return stats
        
    def set_bet(self, percentage):
        bet = int(percentage) * self.points / 100
        return bet
    
    def get_ranking(self):
        ranking = CustomUser.objects.filter(points__gt=self.points).count() + 1
        return ranking
    
    class Meta:
        db_table = 'user'
        verbose_name_plural = 'Users' 