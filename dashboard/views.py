import datetime

from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from mongoengine import ValidationError, DoesNotExist, MultipleObjectsReturned

from application.models import *

from dashboard.utils import import_volunteer, create_volunteering_date, \
    volunteer_date_register


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

    volunteer_id = request.GET.get('id')
    # if there's no user_id, redirect back to manage volunteers page
    if not request.GET.get('id'):
        return redirect('dashboard.views.manage_volunteers')

    # handle volunteer user editing/deleting
    try:
        volunteer = WIS_User.objects.get(id=volunteer_id)
        params = {
            'volunteer': volunteer,
        }
        return render_to_response(
            'admin/view_volunteer.html', params,
            context_instance=RequestContext(request)
        )
    except DoesNotExist:
        return redirect('dashboard.views.manage_volunteers')


@login_required
def manage_dates(request):
    # send regular users back to dashboard
    if request.user.is_volunteer:
        return redirect('dashboard.views.dashboard')

    # handle volunteer date add/editing
    success, error = ('',)*2
    try:
        if request.method == 'POST':
            type = request.POST.get('type')
            if type == 'single':
                # get form data
                date = request.POST.get('date')
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                slots = request.POST.get('slots')
                # create the object
                success, error = create_volunteering_date(date, start_time, end_time, slots)
            elif type == 'csv':
                # create vars to keep track of successes and errors
                num_success = 0
                error_dates = []
                # parse csv file
                csv_date_list = request.FILES.get('csv_date_list')
                date_list = csv_date_list.read().split('\r')
                for volunteer_date in date_list:
                    volunteer_date = volunteer_date.split(',')
                    date = volunteer_date[0]
                    start_time = volunteer_date[1]
                    end_time = volunteer_date[2]
                    slots = volunteer_date[3]
                    date_success, date_error = create_volunteering_date(
                        date, start_time, end_time, slots
                    )
                    if date_success:
                        num_success+=1
                    if date_error:
                        error_dates.append(date)
                if num_success:
                    success = 'Successfully added %s volunteering dates'\
                          % num_success
                if error_dates:
                    error = 'Unable to add the following dates:'
                    for error_date in error_dates:
                        error += '\n %s' % error_date
            else:
                error = 'Unable to process request'
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

    date_id = request.GET.get('id')
    # if there's no date_id, redirect back to manage dates page
    if not request.GET.get('id'):
        return redirect('dashboard.views.manage_dates')

    # handle volunteer date reports/editing/deleting
    try:
        volunteer_date = Volunteer_Date.objects.get(id=date_id)
        registrations = Volunteer_Date_Registration.objects(volunteer_date=
                                                            volunteer_date)
        params = {
            'volunteer_date': volunteer_date,
            'registrations': registrations,
        }
        return render_to_response(
            'admin/view_date.html', params,
            context_instance=RequestContext(request)
        )
    except DoesNotExist:
        return redirect('dashboard.views.manage_dates')


@login_required
def volunteer_register(request):
    success, error = ('',)*2
    volunteer = request.user

    # handle volunteer date registration
    if request.method == 'POST':
        date_id = request.POST.get('date_id')
        success, error = volunteer_date_register(volunteer.id, date_id)

    dates = Volunteer_Date.objects
    params = {
        'success': success,
        'error': error,
        'dates': dates,
    }
    return render_to_response(
        'volunteers/volunteer_register.html', params,
        context_instance=RequestContext(request)
    )


@login_required
def volunteer_manage_registrations(request):
    params = {
        'user': request.user,
    }
    return render_to_response(
        'volunteers/volunteer_manage_registrations.html', params,
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
