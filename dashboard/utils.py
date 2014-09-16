from django.core.validators import validate_email

from application.models import *


def import_volunteer(email, first_name, last_name):
    success, error = ('',)*2
    if email and first_name and last_name:
        try:
            validate_email(email)
            # check to make sure user is new and unique
            unique_user = True
            try:
                Allowed_User.objects.get(email=email)
                unique_user = False
            except DoesNotExist:
                pass
            try:
                WIS_User.objects.get(email=email)
                unique_user = False
            except DoesNotExist:
                pass

            if unique_user:
                new_user = Allowed_User()
                new_user.email = email
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()
                # TODO: send email with signup link
                success = 'Sent email to %s for account activation'\
                          % new_user.email
            else:
                error = 'A volunteer with that email already exists'
        except:
            error = 'Invalid email address'
    else:
        error = 'Please fill out all fields'
    return (success, error,)