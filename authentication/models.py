from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models


class AuthUser(AbstractUser):

    USER_TYPE = [
        ("President", "President"),
        ("Treasurer", "Treasurer"),
        ("Employee", "Employee"),
    ]
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE)

    def __str__(self) -> str:

        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.get_username()

    def get_full_name(self) -> str:
        return super().get_full_name()

    def get_username(self) -> str:
        return super().get_username()
    
    def get_user_type(self) -> str:
        return self.user_type


    def formatted_date(self):
        return self.date_joined.strftime("%b %d, %Y, %I:%M %p").replace("PM", "pm").replace("AM", "am")

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
        db_table = "auth_user"
