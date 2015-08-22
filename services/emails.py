# Email sending service
from django.core.mail import EmailMultiAlternatives


def send_email(to, subject, message):
    text_content = message
    from_email = 'wis@mcabayarea.org'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
