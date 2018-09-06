from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import *


@receiver(post_delete, sender=Volunteer_Date)
def auto_delete_registrations_with_date(sender, instance, **kwargs):
    if instance.registrations:
        instance.registrations.all().delete()


@receiver(post_delete, sender=WIS_User)
def auto_delete_registrations_with_user(sender, instance, **kwargs):
    if instance.registrations:
        instance.registrations.all().delete()
