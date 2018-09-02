from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.validators import validate_email
from django.contrib.auth.models import User as DjangoUserClass

from application.models import *

from services.emails import send_temporary_password_email


def create_account(request):
    state = ''
    if request.method == 'POST':
        try:
            # get data from form
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            account_type = request.POST.get('type', 'volunteer')

            # validate form data
            if account_type == 'admin':
                if request.POST.get('admin_key') != 'mcawis3003':
                    state = 'Invalid admin sign up key'
            else:
                # check to see if volunteer user is allowed
                try:
                    Allowed_User.objects.get(email=email)
                except:
                    state = 'Email not registered with WIS. ' \
                            'Please contact the admin for help.'

            # check to make sure user is unique
            if not state:
                try:
                    WIS_User.objects.get(email=email)
                    state = 'A user with that email already exists'
                except:
                    pass

            # validate email address
            if not state:
                try:
                    validate_email(email)
                except:
                    state = 'Invalid email address'

            # make sure first and last name are filled
            if not state:
                if not first_name or not last_name:
                    state = 'Please enter a first and last name'

            # make sure password is longer than 8 chars
            if not state:
                if len(password) < 8:
                    state = 'Passwords must be at least 8 characters'

            # check to make sure passwords match
            if not state:
                if password != confirm_password:
                    state = 'Passwords do not match'

            # if no errors, create account and login
            if not state:
                user = WIS_User(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                if account_type == 'admin':
                    user.is_admin = True
                    user.is_volunteer = False
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('dashboard')
        except:
            state = 'Unable to process request'
    params = {
        'state': state
    }
    return render(
        request,
        'signup.html',
        params,
    )


def sign_in(request):
    state = ''
    if request.method == 'POST':
        try:
            user = WIS_User.objects.get(email=request.POST.get('email'))
            if user.check_password(request.POST.get('password')):
                login(request, user)
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                state = "Incorrect username/password combination"
        except:
            print(e)
            state = "User does not exist"
    params = {
        'state': state
    }
    return render(
        request,
        'login.html',
        params,
    )


def forgot_password(request):
    success, error = ('',)*2
    if request.method == 'POST':
        try:
            # get user from db
            user = WIS_User.objects.get(email=request.POST.get('email'))
            # create a temporary password
            temp_password = DjangoUserClass.objects.make_random_password(length=8)
            user.set_password(temp_password)
            # email temporary password to user
            send_temporary_password_email(user, temp_password)
            success = "A temporary password has been emailed to you"
        except:
            error = "User does not exist"
    params = {
        'success': success,
        'error': error
    }
    return render(
        request,
        'forgot.html',
        params,
    )


def logout_user(request):
    logout(request)
    return redirect('sign_in')
