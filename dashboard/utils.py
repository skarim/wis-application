from django.core.validators import validate_email

from services.emails import send_email
from services.localization import localize, get_diff_from_now
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
            # parse values
            event_begin = localize(date, start_time)
            event_end = localize(date, end_time)
            slots_total = int(slots)

            # handle errors
            if event_begin >= event_end:
                error = 'End time must be after start time'
            elif slots_total < 1:
                error = 'Must have at least one slot per volunteer date'
            else:
                new_date = Volunteer_Date(event_begin=event_begin,
                                          event_end=event_end,
                                          slots_total=slots_total)
                new_date.save()
                print 'new_date begin: {0}'.format(new_date.event_begin)
                print 'new_date end: {0}'.format(new_date.event_end)
                success = 'Added a volunteering date on %(d)s with %(s)s slots'\
                          % {'d': date, 's':slots}
        except:
            error = 'An unexpected error occurred. Please try again.'
    else:
        error = 'Please fill out all fields'
    return (success, error,)


def volunteer_date_register(volunteer_id, date_id):
    success, error = ('',)*2
    if volunteer_id and date_id:
        try:
            volunteer_user = WIS_User.objects.get(id=volunteer_id)
            volunteer_date = Volunteer_Date.objects.get(id=date_id)
            if volunteer_date.slots_available < 1:
                error = 'There are no slots available for that date'
            elif volunteer_date.is_past:
                error = 'You cannot signup for a date that has already passed'
            elif get_diff_from_now(volunteer_date.event_begin) < 48:
                error = 'You cannot signup for a date less than 48 hours in advance'
            elif volunteer_user in volunteer_date.volunteers:
                error = 'You have already registered for this date'
            else:
                # create registration object
                registration = Volunteer_Date_Registration(volunteer_date=
                                                           volunteer_date)
                registration.save()

                # add registration to the volunteer's list
                volunteer_user.registrations.append(registration)
                volunteer_user.signup_count+=1
                volunteer_user.save()

                # add volunteer to list of volunteers for the date
                volunteer_date.volunteers.append(volunteer_user)
                volunteer_date.save()

                success = 'You have successfully signed up for volunteering on ' \
                          'the selected date'
        except DoesNotExist:
            error = 'Selected date does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)
