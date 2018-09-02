from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from services.timing import localize
from services.emails import send_volunteer_reminder_email
from application.models import *


class Command(BaseCommand):
    help = 'Sends email reminders to volunteers who have signed up for a ' \
           'volunteering date within the next N hours'

    option_list = BaseCommand.option_list + (
            make_option('--hours_from_now',
                action='store_true',
                dest='hours_from_now',
                default=168,
                help='Set value for N, where email reminders are sent to '
                     'volunteers who have signed up for a volunteering date '
                     'within the next N hours'),
            )

    def handle(self, *args, **options):
        try:
            hours_from_now = options.get('hours_from_now')
            volunteer_dates = Volunteer_Date.objects.get()
            num_emails_sent = 0

            for volunteer_date in volunteer_dates:
                # check if volunteer_date is in the future and within hours_from_now
                if 0 < get_diff_from_now(volunteer_date.event_begin) < hours_from_now:
                    # localize the volunteer date times for emailing
                    localized_start = localize(volunteer_date.event_begin)
                    localized_end = localize(volunteer_date.event_end)

                    # send volunteers reminder emails
                    for volunteer in volunteer_date.volunteers:
                        send_volunteer_reminder_email(volunteer,
                                                      localized_start,
                                                      localized_end)
                        num_emails_sent+=1

            self.stdout.write('Successfully emailed %d volunteers with '
                              'registrations %d hours from now' %
                              (num_emails_sent, hours_from_now))
        except Exception as e:
            raise CommandError('Error sending emails: %s' % e)
