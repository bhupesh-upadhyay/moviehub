from celery import shared_task
from time import sleep
from .services import UserService, AuthService


# TODO:
"""
Image processing: You might want to resize avatar images that users upload or apply some encoding on all images that users can share on your platform. Image processing is often a resource-intensive task that can slow down your web app, mainly if you’re serving a large community of users.
Text processing: If you allow users to add data to your app, then you might want to monitor their input. For example, you may want to check for profanity in comments or translate user-submitted text to a different language. Handling all this work in the context of your web app can significantly impair performance.
"""

@shared_task
def send_welcome_email(email):
    print('start')
    sleep(6)
    print(f"Sending welcome email to {email}")
    print('end')
    return 'Email sent successfully'

"""
acks_late=True   → acknowledge after completion
max_retries=3    → retry if failure occurs

Default Behavior: Queue -> Worker takes task -> ACK immediately -> Worker crashes -> Task lost ❌
With acks_late=True: Queue -> Worker takes task -> Worker crashes -> Task returned to queue -> Another worker executes

production:
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    acks_late=True
)
"""

@shared_task(bind=True, acks_late=True, max_retries=3)
def send_welcome_email(self, email):
    print(f"Sending email to {email}")


@shared_task
def send_verification_email_task(user_id):
    sleep(5)
    UserService.send_verification_email(user_id)
    
@shared_task
def send_password_reset_email_task(user_id):
    sleep(8)
    AuthService.send_password_reset_email(user_id)