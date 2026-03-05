# Signals allow certain senders to notify receivers when an action happens.

# Some common Django model signals:
# Signal	Triggered When
# pre_save	Before model is saved
# post_save	After model is saved
# pre_delete	Before delete
# post_delete	After delete

"""
Signals should be used for things that are OK to fail without breaking the system.
    User creation MUST succeed
    Email sending can fail
    Analytics can fail
That's the correct place for signals.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):

    if created:
        print(f"Welcome email sent to {instance.email}")