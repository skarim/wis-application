from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        WIS_User.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.wis_user.save()


@receiver(post_delete, sender=Volunteer_Date)
def auto_delete_registrations_with_date(sender, instance, **kwargs):
    if instance.registrations:
        instance.registrations.all().delete()


@receiver(post_delete, sender=WIS_User)
def auto_delete_registrations_with_user(sender, instance, **kwargs):
    if instance.registrations:
        instance.registrations.all().delete()
