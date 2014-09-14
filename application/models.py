# coding=utf-8
from mongoengine import Document, StringField, URLField, DateTimeField, \
    EmbeddedDocument, ListField, ReferenceField, BooleanField, IntField, \
    EmbeddedDocumentField, DoesNotExist, ValidationError
from mongoengine.django.auth import User


class VolunteerDate(Document):
    event_date = DateTimeField()
    event_begin = DateTimeField()
    event_end = DateTimeField()
    slots_total = IntField()
    slots_available = IntField()
    volunteers = ListField(ReferenceField('VolunteerUser'))


class VolunteerUser(User):
    signup_count = IntField(default=0)
    registrations = ListField(ReferenceField(VolunteerDate))
    # newsletter = BooleanField(default=False)
    # is_admin = BooleanField(default=False)
    # is_creator = BooleanField(default=False)
    # is_analyst = BooleanField(default=False)
    # act_code = StringField()