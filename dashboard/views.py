import datetime

from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from mongoengine import ValidationError, DoesNotExist, MultipleObjectsReturned

from application.models import *

from dashboard.utils import import_volunteer


@login_required
def dashboard(request):
    return render_to_response(
        'dashboard.html',
        context_instance=RequestContext(request)
    )


@login_required
def manage_volunteers(request):
    # send regular users back to dashboard
    if request.user.is_volunteer:
        return redirect('dashboard.views.dashboard')

    # handle volunteer add/import
    success, error = ('',)*2
    try:
        if request.method == 'POST':
            type = request.POST.get('type')
            if type == 'single':
                email = request.POST.get('email')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                success, error = import_volunteer(email, first_name, last_name)
            elif type == 'csv':
                # create vars to keep track of successes and errors
                num_success = 0
                error_users = []
                # parse csv file
                csv_user_list = request.FILES.get('csv_user_list')
                user_list = csv_user_list.read().split('\r')
                for user in user_list:
                    user = user.split(',')
                    email = user[2]
                    first_name = user[0]
                    last_name = user[1]
                    user_success, user_error = import_volunteer(
                        email, first_name, last_name
                    )
                    if user_success:
                        num_success+=1
                    if user_error:
                        error_users.append(email)
                if num_success:
                    success = 'Sent emails to %s users for account activation'\
                          % num_success
                if error_users:
                    error = 'Unable to add the following emails:'
                    for error_user in error_users:
                        error += '\n %s' % error_user
            else:
                error = 'Unable to process request'
    except:
        error = 'Unable to process request'

    users = WIS_User.objects
    params = {
        'success': success,
        'error': error,
        'users': users,
    }
    return render_to_response(
        'admin/manage_volunteers.html', params,
        context_instance=RequestContext(request)
    )


@login_required
def view_volunteer(request):
    # send regular users back to dashboard
    if request.user.is_volunteer:
        return redirect('dashboard.views.dashboard')

    # if there's no user_id, redirect back to manage volunteers page
    if not request.GET.get('id'):
        return redirect('dashboard.views.manage_volunteers')

    # handle volunteer user editing/deleting
    return render_to_response(
        'admin/view_volunteer.html',
        context_instance=RequestContext(request)
    )


@login_required
def manage_dates(request):
    # send regular users back to dashboard
    if request.user.is_volunteer:
        return redirect('dashboard.views.dashboard')

    # handle volunteer date add/editing
    success, error = ('',)*2
    try:
        if request.method == 'POST':
            # get form data
            date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            slots = request.POST.get('slots')
            # create the object
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
        error = 'Error adding event'
    dates = Volunteer_Date.objects
    params = {
        'success': success,
        'error': error,
        'dates': dates,
    }
    return render_to_response(
        'admin/manage_dates.html', params,
        context_instance=RequestContext(request)
    )


@login_required
def view_date(request):
    # send regular users back to dashboard
    if request.user.is_volunteer:
        return redirect('dashboard.views.dashboard')

    # if there's no date_id, redirect back to manage dates page
    if not request.GET.get('id'):
        return redirect('dashboard.views.manage_dates')

    # handle volunteer date reports/editing/deleting
    return render_to_response(
        'admin/view_date.html',
        context_instance=RequestContext(request)
    )


@login_required
def account_settings(request):
    success, error = ('',)*2
    try:
        if request.method == 'POST':
            user = request.user
            identifier = request.POST.get('identifier')
            # update name
            if identifier == 'name':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                if first_name and last_name:
                    try:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()
                        success = 'Name successfully updated to %s' \
                                  % ' '.join([first_name, last_name])
                    except:
                        error = 'Error saving new name'
                else:
                    error = 'You must enter both a first and last name'
            # update email address
            elif identifier == 'email':
                email = request.POST.get('email')
                if email:
                    try:
                        validate_email(email)
                        try:
                            WIS_User.objects.get(email=email, is_active=True)
                            error = 'That email address is already in use'
                        except DoesNotExist:
                            user.email = email
                            user.save()
                            success = 'Email successfully updated to %s' % email
                    except ValidationError:
                        error = 'You must enter a valid email address'
                else:
                    error = 'You must enter an email address'
            # update password
            elif identifier == 'password':
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                if old_password and new_password and confirm_password:
                    if user.check_password(old_password):
                        if new_password == confirm_password:
                            user.set_password(new_password)
                            user.save()
                            success = 'Password successfully changed'
                        else:
                            error = 'New passwords do not match'
                    else:
                        error = 'Current password incorrect'
                else:
                    error = 'You must fill in all the fields before submitting'
            else:
                error = 'Invalid submission'
    except:
        error = 'Error saving changes'
    params = {
        'success': success,
        'error': error
    }
    return render_to_response(
        'settings.html', params,
        context_instance=RequestContext(request)
    )