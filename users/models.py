from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    #We want 3 roles: Admin (Superuser), Vendor, Customer
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('vendor','Vendor'),
        ('customer','Customer'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

