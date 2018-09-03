import datetime
from django.db import models
from django.contrib.auth.models import User

from services.timing import get_diff_from_now


class Volunteer_Date(models.Model):
    category = models.TextField()
    event_begin = models.DateTimeField()
    event_end = models.DateTimeField()
    slots_total = models.IntegerField(default=0)

    @property
    def is_past(self):
        return get_diff_from_now(self.event_end) < 0

    @property
    def is_one_week_or_less_prior(self):
        return get_diff_from_now(self.event_begin) < 168

    @property
    def is_two_days_or_less_prior(self):
        return get_diff_from_now(self.event_begin) < 48

    @property
    def slots_available(self):
        return self.slots_total - self.slots_filled

    @property
    def slots_filled(self):
        try:
            return self.registrations.filter(cancelled=False).count()
        except:
            return 0

    @property
    def num_registrations(self):
        try:
            return self.registrations.count()
        except:
            return 0

    def check_if_user_registered(self, user):
        try:
            if self.registrations.filter(volunteer=user, cancelled=False).count() > 0:
                return True
            else:
                return False
        except:
            return False


class Volunteer_Date_Registration(models.Model):
    volunteer = models.ForeignKey('WIS_User', related_name='registrations', on_delete=models.DO_NOTHING,)
    volunteer_date = models.ForeignKey(Volunteer_Date, related_name='registrations', on_delete=models.DO_NOTHING,)
    marked = models.BooleanField(default=False) # whether an attended/absent value has been set by the admin
    attended = models.BooleanField(default=False)
    signup_time = models.DateTimeField(default=datetime.datetime.utcnow)
    cancelled = models.BooleanField(default=False)
    cancel_time = models.DateTimeField(blank=True, null=True)


class WIS_User(User):
    is_admin = models.BooleanField(default=False)
    is_volunteer = models.BooleanField(default=True)

    @property
    def signup_count(self):
        try:
            return self.registrations.count()
        except:
            return 0

    @property
    def completed_count(self):
        try:
            return self.registrations.filter(marked=True, attended=True).count()
        except:
            return 0

    @property
    def missed_count(self):
        try:
            return self.registrations.filter(marked=True, attended=False).count()
        except:
            return 0


class Allowed_User(models.Model):
    email = models.TextField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()


# signals for pre/post create/save/delete actions
from .signals import *
