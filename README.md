# WIS Volunteer Application
MCA Weekend Islamic School Volunteer Scheduling Application


### Set Up the Virtual Environment
    virtualenv venv
    source venv/bin/activate

### Install Dependencies
    pip install -r requirements.txt

### Run Server Locally
    python manage.py runserver

### Send Reminder Emails
    python manage.py email_reminders --hours_from_now 168
The optional `hours_from_now` flag sets the value for N, where email reminders 
are sent to volunteers who have signed up for a volunteering date within the 
next N hours.

_The default value is 168 hours (1 week)_
