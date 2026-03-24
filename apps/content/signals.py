from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction

from .models import Movie
from .tasks import generate_movie_embedding

# TODO: run on updating the title and description field.
# pre_save = fetches old title and description
# post_save = new entry created or if old then checks the title and description change post addes in celery.

@receiver(pre_save, sender=Movie)
def store_old_values(sender, instance, **kwargs):
    print('Triggred presave fetching old title and description')
    if instance.pk:
        old = Movie.objects.get(pk=instance.pk)
        instance._old_title = old.title
        instance._old_description = old.description

@receiver(post_save, sender=Movie)
def generate_embedding(sender, instance, created, **kwargs):
    if created:
        trigger = True
    else:
        trigger = (
            getattr(instance, "_old_title", None) != instance.title or
            getattr(instance, "_old_description", None) != instance.description
        )

    if trigger:
        print('Triggred postsave adding movie to the queue.')
        transaction.on_commit(
            lambda: generate_movie_embedding.delay(instance.id)
        )
