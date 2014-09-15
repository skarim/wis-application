# coding=utf-8
from mongoengine import Document, StringField, URLField, DateTimeField, \
    EmbeddedDocument, ListField, ReferenceField, BooleanField, IntField, \
    EmbeddedDocumentField, DoesNotExist, ValidationError
from mongoengine.django.auth import User


class Volunteer_Date(Document):
    event_date = DateTimeField()
    event_begin = DateTimeField()
    event_end = DateTimeField()
    slots_total = IntField()
    slots_available = IntField()
    volunteers = ListField(ReferenceField('VolunteerUser'))


class WIS_User(User):
    is_admin = BooleanField(default=False)
    is_volunteer = BooleanField(default=True)
    # volunteer data fields
    signup_count = IntField(default=0)
    completed_count = IntField(default=0)
    missed_count = IntField(default=0)
    registrations = ListField(ReferenceField(Volunteer_Date))
    # newsletter = BooleanField(default=False)
    # is_admin = BooleanField(default=False)
    # is_creator = BooleanField(default=False)
    # is_analyst = BooleanField(default=False)
    # act_code = StringField()

class Allowed_User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()