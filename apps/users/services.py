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
from apps.users.models import UserProfile
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import email_verification_token
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class UserService:

    @staticmethod
    def create_user(validated_data):
        """
        Creates a user and profile inside a transaction
        and sends an email verification link.
        """
        from .tasks import send_verification_email_task #lazy import: avoids circular import
        with transaction.atomic():
            # is because passwords must be hashed, not saved as plain text.
            password = validated_data.pop("password")
            user = User.objects.create_user(password=password, **validated_data)
            UserProfile.objects.create(user=user)

        transaction.on_commit(
            lambda: send_verification_email_task.delay(user.id)
        )

        return user
    
    @staticmethod
    def send_verification_email(user_id):
        user = User.objects.get(id=user_id) # should not pass object because celery serializer arguments
        # generate verification token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        verification_url = reverse(
            "verify-email",
            kwargs={
                "uid": uid,
                "token": token
            }
        )

        verification_link = f"{settings.DOMAIN}{verification_url}"

        # send email
        send_mail(
            subject="Verify your email",
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
    
class AuthService:
    @staticmethod
    def send_password_reset_email(email):
        try:
            user = User.objects.get(email=email)   
        except User.DoesNotExist:
            return
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))    
        token = email_verification_token.make_token(user)
        
        reset_url = reverse('reset-password', kwargs={'uid':uid, 'token':token})
        reset_link = f"{settings.DOMAIN}{reset_url}"
        
        print('Password reset link: ', reset_link)

# TODO: AuthService.login_user()
"""record login history
update last_login
check rate limits
trigger analytics
lock accounts after failures"""

if __name__ == '__main__':
    pass
    # send_welcome_email.delay(user.email)