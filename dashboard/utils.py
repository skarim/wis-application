from django.core.validators import validate_email

from services.emails import send_email
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
                send_welcome_email(new_user)
                success = 'Sent email to %s for account activation'\
                          % new_user.email
            else:
                error = 'A volunteer with that email already exists'
        except:
            error = 'Invalid email address'
    else:
        error = 'Please fill out all fields'
    return (success, error,)


def send_welcome_email(user):
    activate_link = 'http://app.mcawis.org/activate/?email={0}&first_name={2}' \
                    '&last_name={3}'.format(user.email, user.first_name,
                                            user.last_name)
    email_message = 'Dear {0} {2}, \n\nAssalamuAlaikum \n\nAn account has been ' \
                    'created for you on the WIS Volunteer Scheduling website. ' \
                    'Please go to {0} to activate up your account and set your ' \
                    'password. After activating your account, you can login at ' \
                    'http://app.mcawis.org. If you have any questions, please ' \
                    'contact the admin at wis@mcabayarea.org.\n\nJazakAllah ' \
                    'Khairan \nWIS Admin'.format(user.first_name,
                                                 user.last_name, activate_link)
    send_email(user.email, 'Activate your WIS Volunteer Account', email_message)


def create_volunteering_date(date, start_time, end_time, slots):
    success, error = ('',)*2
    if date and start_time and end_time and slots:
        try:
            new_date = Volunteer_Date(date, start_time, end_time, slots)
            # handle errors
            if new_date.event_begin >= new_date.event_end:
                error = 'End time must be after start time'
            elif new_date.slots_total < 1:
                error = 'Must have at least one slot per volunteer date'
            else:
                new_date.save()
                success = 'Added a volunteering date on %(d)s with %(s)s slots'\
                          % {'d': date, 's':slots}
        except:
            error = 'An unexpected error occurred. Please try again.'
    else:
        error = 'Please fill out all fields'
    return (success, error,)
