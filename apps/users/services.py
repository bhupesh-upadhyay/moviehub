# Buisness logic create user
"""
Create user (hashed password)
Maybe create profile (future)
Maybe send verification email (future)
Return response

Service creates user
↓
Triggers domain event
↓
Listeners handle side effects

In Django terms:
Service creates user
After commit → trigger Celery task
Logging handled separately
Email handled async

Because
API View can call it
Admin action can call it
CLI command can call it
Celery task can call it
Future microservice can call it
"""
from apps.users.models import User, UserProfile
from django.db import transaction
from django.contrib.auth import get_user_model

class UserService:

    @staticmethod
    def create_user(validated_data):
        # is because passwords must be hashed, not saved as plain text.
        password = validated_data.pop("password")
        with transaction.atomic():
            user = User.objects.create_user(password=password, **validated_data)
            user.profile = UserProfile.objects.create(user=user)
            
        return user
