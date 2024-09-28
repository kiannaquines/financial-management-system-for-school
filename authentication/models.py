from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models

class AuthUser(AbstractUser):

    USER_TYPE = [
        ('President','President'),
        ('Treasurer','Treasurer'),
        ('Employee','Employee')
    ]

    user_type = models.CharField(max_length=50,choices=USER_TYPE)
    
    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
        db_table = 'auth_user'
    




