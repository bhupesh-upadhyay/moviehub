from celery import shared_task
from time import sleep

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