# coding=utf-8
from mongoengine import Document, StringField, URLField, DateTimeField, \
    EmbeddedDocument, ListField, ReferenceField, BooleanField, IntField, \
    EmbeddedDocumentField, DoesNotExist, ValidationError
from mongoengine.django.auth import User

import datetime


class Volunteer_Date(Document):
    event_begin = DateTimeField()
    event_end = DateTimeField()
    slots_total = IntField()
    volunteers = ListField(ReferenceField('WIS_User'))

    @property
    def is_past(self):
        if datetime.date.today() > self.event_end.date():
            return True
        return False

    @property
    def slots_available(self):
        return int(self.slots_total) - len(self.volunteers)

    @property
    def slots_filled(self):
        return len(self.volunteers)


class Volunteer_Date_Registration(Document):
    volunteer_date = ReferenceField(Volunteer_Date)
    signed_up = BooleanField(default=True)
    attended = BooleanField(default=False)


class WIS_User(User):
    is_admin = BooleanField(default=False)
    is_volunteer = BooleanField(default=True)
    # volunteer data fields
    signup_count = IntField(default=0)
    completed_count = IntField(default=0)
    missed_count = IntField(default=0)
    registrations = ListField(ReferenceField(Volunteer_Date))


class Allowed_User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()