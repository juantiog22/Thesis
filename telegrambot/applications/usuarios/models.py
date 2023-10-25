from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD='username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_short_name(self):
        return self.username
    

class Suscriber(models.Model):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )
    
    chatid = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    def __str__(self):
        return self.name 


    def get_id(self):
        return self.id

    def get_username(self):
        return self.username
    
    def get_name(self):
        return self.name