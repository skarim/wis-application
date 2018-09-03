from django.core.validators import validate_email

from services.emails import send_welcome_email, send_date_registered_email, \
    send_date_cancelled_email, send_admin_date_cancelled_email, \
    send_admin_date_deleted_email, send_date_attended_email,\
    send_date_absent_email
from services.timing import universalize, localize
from application.models import *


def import_volunteer(email, first_name, last_name):
    success, error = ('',)*2
    if email and first_name and last_name:
        validate_email(email)
        # check to see if user is already in the system
        user_exists = False
        try:
            Allowed_User.objects.get(email=email)
            user_exists = True
        except:
            pass

        if not user_exists:
            try:
                # send email even if already been invited previously
                new_user = Allowed_User.objects.get(email=email)
            except:
                new_user = Allowed_User()
                new_user.email = email
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()
            send_welcome_email(new_user)
            success = 'Sent email to %s for account activation'\
                      % new_user.email
        else:
            error = 'An account with that email already exists'
    else:
        error = 'Please fill out all fields'
    return (success, error,)


def create_volunteering_date(category, date, start_time, end_time, slots):
    success, error = ('',)*2
    if category and date and start_time and end_time and slots:
        # parse values
        event_begin = universalize(date, start_time)
        event_end = universalize(date, end_time)
        slots_total = int(slots)

        # handle errors
        if event_begin >= event_end:
            error = 'End time must be after start time'
        elif slots_total < 1:
            error = 'Must have at least one slot per volunteer date'
        else:
            new_date = Volunteer_Date(category=category,
                                      event_begin=event_begin,
                                      event_end=event_end,
                                      slots_total=slots_total)
            new_date.save()
            success = 'Added a volunteering date on %(d)s with %(s)s slots'\
                      % {'d': date, 's':slots}
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
            elif volunteer_date.is_two_days_or_less_prior:
                error = 'You cannot signup for a date less than 48 hours in advance'
            elif volunteer_date.check_if_user_registered(volunteer_user):
                error = 'You have already registered for this date'
            else:
                # create registration object
                registration = Volunteer_Date_Registration(volunteer_date=volunteer_date,
                                                           volunteer=volunteer_user)
                registration.save()

                # localize the volunteer date times for displaying
                localized_start = localize(volunteer_date.event_begin)
                localized_end = localize(volunteer_date.event_end)

                # send confirmation email
                send_date_registered_email(volunteer_user, localized_start, localized_end)

                success = 'You have successfully signed up for volunteering on ' \
                          '{0} from {1} to {2}'.format(localized_start.strftime('%A, %B %-d, %Y'),
                                                       localized_start.strftime('%-I:%M %p'),
                                                       localized_end.strftime('%-I:%M %p'))
        except:
            error = 'Selected date does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def volunteer_date_cancellation(volunteer_id, date_id):
    success, error = ('',)*2
    if volunteer_id and date_id:
        volunteer_user = WIS_User.objects.get(id=volunteer_id)
        volunteer_date = Volunteer_Date.objects.get(id=date_id)
        volunteer_registration = Volunteer_Date_Registration.objects.get(volunteer_date=volunteer_date,
                                                                         volunteer=volunteer_user)

        if volunteer_date.is_past:
            error = 'You cannot cancel registration for a date that has already passed'
        elif volunteer_date.is_two_days_or_less_prior:
            error = 'You cannot cancel registration for a date less than 1 week in advance'
        elif volunteer_registration.cancelled:
            error = 'You have already cancelled this registration'
        else:
            # set registration to cancelled
            volunteer_registration.cancelled = True
            volunteer_registration.cancel_time = datetime.datetime.utcnow()
            volunteer_registration.save()

            # localize the volunteer date times for displaying
            localized_start = localize(volunteer_date.event_begin)
            localized_end = localize(volunteer_date.event_end)

            # send confirmation email
            send_date_cancelled_email(volunteer_user, localized_start, localized_end)

            success = 'You have successfully cancelled your volunteering registration on ' \
                      '{0} from {1} to {2}'.format(localized_start.strftime('%A, %B %-d, %Y'),
                                                   localized_start.strftime('%-I:%M %p'),
                                                   localized_end.strftime('%-I:%M %p'))
    else:
        error = 'Incomplete form data'
    return (success, error,)


def admin_remove_volunteer_from_date(registration_id):
    success, error = ('',)*2
    if registration_id:
        try:
            volunteer_registration = Volunteer_Date_Registration.objects.get(id=registration_id)
            volunteer_date = volunteer_registration.volunteer_date
            volunteer_user = volunteer_registration.volunteer

            # update the registration object
            volunteer_registration.cancelled = True
            volunteer_registration.cancel_time = datetime.datetime.utcnow()
            volunteer_registration.save()

            # localize the volunteer date times for emailing
            localized_start = localize(volunteer_date.event_begin)
            localized_end = localize(volunteer_date.event_end)

            # send notification email
            send_admin_date_cancelled_email(volunteer_user, localized_start, localized_end)

            success = 'Successfully removed {0} {1} from volunteering date'.format(volunteer_user.first_name,
                                                                                   volunteer_user.last_name)
        except:
            error = 'Registration does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def admin_set_volunteer_attendance(registration_id, attendance_state):
    success, error = ('',)*2
    if registration_id and attendance_state:
        try:
            volunteer_registration = Volunteer_Date_Registration.objects.get(id=registration_id)
            volunteer_date = volunteer_registration.volunteer_date
            volunteer_user = volunteer_registration.volunteer

            # set appropriate attendance state
            if attendance_state == 'yes':
                volunteer_registration.attended = True
            else:
                volunteer_registration.attended = False
            volunteer_registration.marked = True

            volunteer_registration.save()

            # localize the volunteer date times for emailing
            localized_start = localize(volunteer_date.event_begin)
            localized_end = localize(volunteer_date.event_end)

            # send notification email
            if volunteer_registration.attended:
                send_date_attended_email(volunteer_user, localized_start, localized_end)
            else:
                send_date_absent_email(volunteer_user, localized_start, localized_end)

            success = 'Successfully saved attendance state for {0} {1}'.format(volunteer_user.first_name,
                                                                               volunteer_user.last_name)
        except:
            error = 'Registration does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def admin_delete_volunteering_date(date_id):
    success, error = ('',)*2
    if date_id:
        volunteer_date = Volunteer_Date.objects.get(id=date_id)

        # localize the volunteer date times for emailing
        localized_start = localize(volunteer_date.event_begin)
        localized_end = localize(volunteer_date.event_end)

        # send emails to all registered volunteers
        for registration in volunteer_date.registrations.filter(cancelled=False):
            send_admin_date_deleted_email(registration.volunteer,
                                          localized_start,
                                          localized_end)

        # finally, delete volunteer_date object
        volunteer_date.delete()

        success = 'Successfully deleted volunteering date on ' \
                  '{0} from {1} to {2}'.format(localized_start.strftime('%A, %B %-d, %Y'),
                                               localized_start.strftime('%-I:%M %p'),
                                               localized_end.strftime('%-I:%M %p'))
    else:
        error = 'Incomplete form data'
    return (success, error,)
