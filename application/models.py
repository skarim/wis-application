# coding=utf-8
from mongoengine import Document, StringField, URLField, DateTimeField, \
    EmbeddedDocument, ListField, ReferenceField, BooleanField, IntField, \
    EmbeddedDocumentField, DoesNotExist, ValidationError
from mongoengine.django.auth import User

import datetime

from services.timing import get_diff_from_now


class Volunteer_Date(Document):
    event_begin = DateTimeField()
    event_end = DateTimeField()
    slots_total = IntField()
    volunteers = ListField(ReferenceField('WIS_User'))

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
        return int(self.slots_total) - len(self.volunteers)

    @property
    def slots_filled(self):
        return len(self.volunteers)


class Volunteer_Date_Registration(Document):
    volunteer_date = ReferenceField(Volunteer_Date)
    volunteer = ReferenceField('WIS_User')
    marked = BooleanField(default=False)
    attended = BooleanField(default=False)
    signup_time = DateTimeField(default=datetime.datetime.utcnow)
    cancelled = BooleanField(default=False)
    cancel_time = DateTimeField()


class WIS_User(User):
    is_admin = BooleanField(default=False)
    is_volunteer = BooleanField(default=True)
    # volunteer data fields
    signup_count = IntField(default=0)
    completed_count = IntField(default=0)
    missed_count = IntField(default=0)
    registrations = ListField(ReferenceField(Volunteer_Date_Registration))


class Allowed_User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()