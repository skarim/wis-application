from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.validators import validate_email

from mongoengine import ValidationError, DoesNotExist, MultipleObjectsReturned

from application.models import *
from application.settings import DEBUG


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
                            success = 'Sent email to %s for account activation'\
                                      % new_user.email
                        else:
                            error = 'A volunteer with that email already exists'
                    except:
                        error = 'Invalid email address'
                else:
                    error = 'Please fill out all fields'
            elif type == 'csv':
                pass
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
        'manage_volunteers.html', params,
        context_instance=RequestContext(request)
    )