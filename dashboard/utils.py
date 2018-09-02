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
        # check to make sure user does not already have an account
        user_exists = False
        try:
            WIS_User.get(email=email)
            user_exists = True
        except DoesNotExist:
            pass

        if not user_exists:
            try:
                # send email even if already been invited previously
                new_user = Allowed_User.get(email=email)
            except DoesNotExist:
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
            volunteer_user = WIS_User.get(id=volunteer_id)
            volunteer_date = Volunteer_Date.get(id=date_id)

            if volunteer_date.slots_available < 1:
                error = 'There are no slots available for that date'
            elif volunteer_date.is_past:
                error = 'You cannot signup for a date that has already passed'
            elif volunteer_date.is_two_days_or_less_prior:
                error = 'You cannot signup for a date less than 48 hours in advance'
            elif volunteer_user in volunteer_date.volunteers:
                error = 'You have already registered for this date'
            else:
                # create registration object
                registration = Volunteer_Date_Registration(volunteer_date=volunteer_date,
                                                           volunteer=volunteer_user)
                registration.save()

                # add registration to the volunteer's list
                volunteer_user.registrations.append(registration)
                volunteer_user.save()

                # add volunteer to list of volunteers for the date
                volunteer_date.volunteers.append(volunteer_user)
                volunteer_date.save()

                # localize the volunteer date times for displaying
                localized_start = localize(volunteer_date.event_begin)
                localized_end = localize(volunteer_date.event_end)

                # send confirmation email
                send_date_registered_email(volunteer_user, localized_start, localized_end)

                success = 'You have successfully signed up for volunteering on ' \
                          '{0} from {1} to {2}'.format(localized_start.strftime('%A, %B %-d, %Y'),
                                                       localized_start.strftime('%-I:%M %p'),
                                                       localized_end.strftime('%-I:%M %p'))
        except DoesNotExist:
            error = 'Selected date does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def volunteer_date_cancellation(volunteer_id, date_id):
    success, error = ('',)*2
    if volunteer_id and date_id:
        try:
            volunteer_user = WIS_User.get(id=volunteer_id)
            volunteer_date = Volunteer_Date.get(id=date_id)

            if volunteer_date.is_past:
                error = 'You cannot cancel registration for a date that has already passed'
            elif volunteer_date.is_two_days_or_less_prior:
                error = 'You cannot cancel registration for a date less than 1 week in advance'
            elif volunteer_user not in volunteer_date.volunteers:
                error = 'You are not already registered for this event'
            else:
                # remove registration from the volunteer's list
                for registration in volunteer_user.registrations:
                    if registration.volunteer_date.id == volunteer_date.id:
                        volunteer_user.registrations.remove(registration)
                        # update the registration object
                        volunteer_registration = Volunteer_Date_Registration.get(id=registration.id)
                        volunteer_registration.cancelled = True
                        volunteer_registration.cancel_time = datetime.datetime.utcnow()
                        volunteer_registration.save()
                volunteer_user.save()

                # remove volunteer from list of volunteers for the date
                volunteer_date.volunteers.remove(volunteer_user)
                volunteer_date.save()

                # localize the volunteer date times for displaying
                localized_start = localize(volunteer_date.event_begin)
                localized_end = localize(volunteer_date.event_end)

                # send confirmation email
                send_date_cancelled_email(volunteer_user, localized_start, localized_end)

                success = 'You have successfully cancelled your volunteering registration on ' \
                          '{0} from {1} to {2}'.format(localized_start.strftime('%A, %B %-d, %Y'),
                                                       localized_start.strftime('%-I:%M %p'),
                                                       localized_end.strftime('%-I:%M %p'))
        except DoesNotExist:
            error = 'Selected date does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def admin_remove_volunteer_from_date(registration_id):
    success, error = ('',)*2
    if registration_id:
        try:
            volunteer_registration = Volunteer_Date_Registration.get(id=registration_id)
            volunteer_date = volunteer_registration.volunteer_date
            volunteer_user = volunteer_registration.volunteer

            # update the registration object
            volunteer_registration.cancelled = True
            volunteer_registration.cancel_time = datetime.datetime.utcnow()
            volunteer_registration.save()

            # remove registration from the volunteer's list
            volunteer_user.registrations.remove(volunteer_registration)
            volunteer_user.save()

            # remove volunteer from list of volunteers for the date
            volunteer_date.volunteers.remove(volunteer_user)
            volunteer_date.save()

            # localize the volunteer date times for emailing
            localized_start = localize(volunteer_date.event_begin)
            localized_end = localize(volunteer_date.event_end)

            # send notification email
            send_admin_date_cancelled_email(volunteer_user, localized_start, localized_end)

            success = 'Successfully removed {0} {1} from volunteering date'.format(volunteer_user.first_name,
                                                                                   volunteer_user.last_name)
        except DoesNotExist:
            error = 'Registration does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def admin_set_volunteer_attendance(registration_id, attendance_state):
    success, error = ('',)*2
    if registration_id and attendance_state:
        try:
            volunteer_registration = Volunteer_Date_Registration.get(id=registration_id)
            volunteer_date = volunteer_registration.volunteer_date
            volunteer_user = volunteer_registration.volunteer

            # set appropriate attendance state
            if attendance_state == 'yes':
                volunteer_registration.attended = True
            else:
                volunteer_registration.attended = False
            volunteer_registration.marked = True

            volunteer_user.save()
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
        except DoesNotExist:
            error = 'Registration does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)


def admin_delete_volunteering_date(date_id):
    success, error = ('',)*2
    if date_id:
        try:
            volunteer_date = Volunteer_Date.get(id=date_id)

            # localize the volunteer date times for emailing
            localized_start = localize(volunteer_date.event_begin)
            localized_end = localize(volunteer_date.event_end)

            # remove registrations from volunteer objects
            for volunteer in volunteer_date.volunteers:
                for registration in volunteer.registrations:
                    if registration.volunteer_date.id == volunteer_date.id:
                        volunteer.registrations.remove(registration)
                        registration.delete()
                        # send notification email
                        send_admin_date_deleted_email(volunteer,
                                                      localized_start,
                                                      localized_end)
                volunteer.save()

            # finally, delete volunteer_date object
            volunteer_date.delete()

            success = 'Successfully deleted volunteering date on ' \
                      '{0} from {1} to {2}'.format(localized_start.strftime('%A, %B %-d, %Y'),
                                                   localized_start.strftime('%-I:%M %p'),
                                                   localized_end.strftime('%-I:%M %p'))
        except DoesNotExist:
            error = 'Volunteering date does not exist'
    else:
        error = 'Incomplete form data'
    return (success, error,)
