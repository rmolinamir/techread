import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.profiles.models import Profile
from src.project.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Creating profile for user {instance.email}")
        Profile.objects.create(user=instance)
