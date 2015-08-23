# Email sending service
from django.core.mail import EmailMultiAlternatives


def send_email(to, subject, message):
    text_content = message
    from_email = 'wis@mcabayarea.org'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()


def send_welcome_email(user):
    activate_link = 'http://app.mcawis.org/activate/?email={0}&first_name={1}' \
                    '&last_name={2}'.format(user.email, user.first_name,
                                            user.last_name)
    email_message = 'Dear {0} {1}, \n\nAssalamuAlaikum \n\nAn account has been ' \
                    'created for you on the WIS Volunteer Scheduling website. ' \
                    'Please go to {2} to activate up your account and set your ' \
                    'password. After activating your account, you can login at ' \
                    'http://app.mcawis.org. If you have any questions, please ' \
                    'contact the admin at wis@mcabayarea.org.\n\nJazakAllah ' \
                    'Khairan \nWIS Admin'.format(user.first_name,
                                                 user.last_name, activate_link)
    send_email(user.email, 'Activate your WIS Volunteer Account', email_message)


def send_date_registered_email(user, start, end):
    subject = 'WIS Volunteering Duty on {0}'.format(start.strftime('%A, %B %-d, %Y at %-I:%M %p'))
    email_message = 'Dear {0} {1}, \n\nAssalamuAlaikum \n\n This is a ' \
                    'confirmation email for your volunteering duty on' \
                    '{2}. Please make sure that you are at the school office 15 ' \
                    'minutes prior to get your assignment. You are required to stay ' \
                    'for the entire time until {3}. \n\n Please note that you cannot ' \
                    'change your volunteering registration within 1 week of ' \
                    'the date. If you can no longer make this date, please ' \
                    'update your settings immediately or contact the admin ' \
                    'at wis@mcabayarea.org.\n\nJazakAllah Khairan ' \
                    '\nWIS Admin'.format(user.first_name, user.last_name,
                                         start.strftime('%A, %B %-d, %Y at %-I:%M %p'),
                                         end.strftime('%-I:%M %p'))
    send_email(user.email, subject, email_message)


def send_date_cancelled_email(user, start, end):
    subject = 'WIS Volunteering Duty on {0}'.format(start.strftime('%A, %B %-d, %Y at %-I:%M %p'))
    email_message = 'Dear {0} {1}, \n\nAssalamuAlaikum \n\n This is a ' \
                    'confirmation email that you cancelled your volunteering duty on' \
                    '{2}. If you have any questions or believe this message is an error, ' \
                    'please update your settings immediately and contact the ' \
                    'admin at wis@mcabayarea.org.\n\nJazakAllah Khairan ' \
                    '\nWIS Admin'.format(user.first_name, user.last_name,
                                         start.strftime('%A, %B %-d, %Y at %-I:%M %p'))
    send_email(user.email, subject, email_message)


def send_admin_date_cancelled_email(user, start, end):
    subject = 'WIS Volunteering Duty on {0}'.format(start.strftime('%A, %B %-d, %Y at %-I:%M %p'))
    email_message = 'Dear {0} {1}, \n\nAssalamuAlaikum \n\n This is a ' \
                    'notification email that your volunteering duty on {2} has been cancelled' \
                    'If you have any questions or believe this message is an error, ' \
                    'please contact the admin at wis@mcabayarea.org.\n\nJazakAllah Khairan ' \
                    '\nWIS Admin'.format(user.first_name, user.last_name,
                                         start.strftime('%A, %B %-d, %Y at %-I:%M %p'))
    send_email(user.email, subject, email_message)
