from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    """
    Makes this the email field.
    Because Django authentication backend still uses USERNAME_FIELD.
    Just making email unique is not enough.
    ß"""
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

"""
from django.contrib.auth import get_user_model
User = get_user_model() # This gets the currently active user model

Model Manager
Contains object creation logic.
Example:
User.objects.create_user()
That method lives in the manager.

using create method:
def create(self, validated_data):
    password = validated_data.pop("password")

    user = User.objects.create(**validated_data)
    user.set_password(password)
    user.save()

    return user
"""