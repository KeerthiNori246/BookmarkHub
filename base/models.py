from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    u_id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    description = models.TextField(null=True, blank=True)

    pfp = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

class Preference(models.Model):
    p_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    users = models.ManyToManyField(User, related_name='preferences', blank=True)
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
    
class Board(models.Model):
    b_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name or "Unnamed Board"

class Article(models.Model):
    a_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    preferences = models.ManyToManyField(Preference, related_name='articles', blank=True)
    pic = models.URLField(max_length=500, null=True, blank=True)
    overview = models.CharField(max_length=300, null=True)
    boards = models.ManyToManyField(Board, related_name='articles', blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
    
