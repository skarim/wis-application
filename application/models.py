import datetime
from django.db import models
from django.contrib.auth.models import User

from services.timing import get_diff_from_now


class Volunteer_Date(models.Model):
    category = models.TextField()
    event_begin = models.DateTimeField()
    event_end = models.DateTimeField()
    slots_total = models.IntegerField(default=0)
    # volunteers = models.ManyToManyField(WIS_User)

    # category = StringField(default='School Day')
    # event_begin = DateTimeField()
    # event_end = DateTimeField()
    # slots_total = IntField()
    # volunteers = ListField(ReferenceField('WIS_User'))

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
        return self.slots_total - self.registrations.objects.filter(cancelled=False).count()

    @property
    def slots_filled(self):
        return self.registrations.objects.filter(cancelled=False).count()


class Volunteer_Date_Registration(models.Model):
    volunteer = models.ForeignKey('WIS_User', related_name='registrations', on_delete=models.DO_NOTHING,)
    volunteer_date = models.ForeignKey(Volunteer_Date, related_name='registrations', on_delete=models.DO_NOTHING,)
    marked = models.BooleanField(default=False) # whether an attended/absent value has been set by the admin
    attended = models.BooleanField(default=False)
    signup_time = models.DateTimeField(default=datetime.datetime.utcnow)
    cancelled = models.BooleanField(default=False)
    cancel_time = models.DateTimeField()

    # volunteer_date = ReferenceField(Volunteer_Date)
    # volunteer = ReferenceField('WIS_User')
    # marked = BooleanField(default=False) # whether an attended/absent value has been set by the admin
    # attended = BooleanField(default=False)
    # signup_time = DateTimeField(default=datetime.datetime.utcnow)
    # cancelled = BooleanField(default=False)
    # cancel_time = DateTimeField()


class WIS_User(User):
    is_admin = models.BooleanField(default=False)
    is_volunteer = models.BooleanField(default=True)
    # registrations = ListField(ReferenceField(Volunteer_Date_Registration))

    @property
    def signup_count(self):
        return self.registrations.objects.count()

    @property
    def completed_count(self):
        count = 0
        for registration in self.registrations:
            if registration.marked:
                if registration.attended:
                    count+=1
        return count

    @property
    def missed_count(self):
        count = 0
        for registration in self.registrations:
            if registration.marked:
                if not registration.attended:
                    count+=1
        return count


class Allowed_User(models.Model):
    email = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
